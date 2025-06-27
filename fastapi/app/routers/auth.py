from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from app import models, schemas
from app.dependencies import get_db
from jose import jwt
from datetime import datetime, timedelta
import requests
import urllib.parse
from passlib.context import CryptContext
import traceback


router = APIRouter(tags=["auth"])

# Canvas настройки
CANVAS_CLIENT_ID = "10000000000001"
CANVAS_CLIENT_SECRET = "wRaALYmGAtcGJrfFYW386XLtat8tDJWE7RfmKLNNNP8QyJwkaJ4ABTnTnJhHa3WC"

# В Docker сервисах используем host.docker.internal, а для редиректов на фронт и Canvas — внешний адрес
CANVAS_INTERNAL_DOMAIN = "http://host.docker.internal"  # Для backend (FastAPI в Docker)
CANVAS_EXTERNAL_DOMAIN = "http://172.23.148.229"
REDIRECT_URI = "http://localhost:8000/api/auth/canvas/callback"
FRONTEND_SUCCESS_REDIRECT = "http://localhost:5173/login-success?token="

CANVAS_API_TOKEN = "Bearer NCT22FukTvtChr8mZtVtcveWC9kw4YuJzcU2eNn3Vc8uaQRftGCa8WQNrJfZf9yG"
CANVAS_API_BASE = f"{CANVAS_INTERNAL_DOMAIN}/api/v1"
CANVAS_ACCOUNT_ID = 1

SECRET_KEY = "your_super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
def register_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    # 1. Check in local DB
    existing_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

    # 2. Check in Canvas
    canvas_check = requests.get(
        f"{CANVAS_API_BASE}/accounts/{CANVAS_ACCOUNT_ID}/users",
        headers={"Authorization": CANVAS_API_TOKEN},
        params={"search_term": user_in.email}
    )
    if canvas_check.status_code == 200 and canvas_check.json():
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован в Canvas")

    # 3. Hash password
    hashed_password = pwd_context.hash(user_in.password)

    # 4. Create in Canvas
    canvas_resp = requests.post(
        f"{CANVAS_API_BASE}/accounts/{CANVAS_ACCOUNT_ID}/users",
        headers={
            "Authorization": CANVAS_API_TOKEN,
            "Content-Type": "application/json"
        },
        json={
            "user": {
                "name": f"{user_in.first_name} {user_in.last_name}"
            },
            "pseudonym": {
                "unique_id": user_in.email,
                "password": user_in.password
            },
            "communication_channel": {
                "address": user_in.email,
                "type": "email",
                "skip_confirmation": True
            }
        }
    )

    print("Canvas API Response:")
    print("Status Code:", canvas_resp.status_code)
    print("Response Body:", canvas_resp.text)

    if canvas_resp.status_code == 400:
        canvas_json = canvas_resp.json()
        if "unique_id" in str(canvas_json):
            raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует в Canvas")
        raise HTTPException(status_code=400, detail=f"Ошибка валидации Canvas: {canvas_json}")

    if canvas_resp.status_code >= 300:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при создании пользователя в Canvas: {canvas_resp.text}"
        )

    canvas_user_data = canvas_resp.json()

    # 5. Create in local DB
    new_user = models.User(
        email=user_in.email,
        password_hash=hashed_password,
        role=models.UserRole.volunteer,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Пользователь успешно зарегистрирован",
        "canvas_user_id": canvas_user_data.get("id"),
        "local_user_id": new_user.id
    }


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.get("/login/canvas")
def login_canvas():
    params = {
        "client_id": CANVAS_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
    }
    # Для браузера используем внешний адрес Canvas
    url = f"{CANVAS_EXTERNAL_DOMAIN}/login/oauth2/auth?{urllib.parse.urlencode(params)}"
    print(f"Redirecting to: {url}")
    return RedirectResponse(url)

@router.get("/canvas/callback")
def canvas_callback(
    code: str | None = None,
    error: str | None = None,
    db: Session = Depends(get_db)
):
    if error == "access_denied":
        print("⛔ Пользователь отменил авторизацию в Canvas")
        return RedirectResponse("http://localhost:5173/login?cancelled=true")

    if not code:
        return JSONResponse(status_code=400, content={"detail": "Код авторизации отсутствует"})

    try:
        print("Canvas callback started with code:", code)

        # Получение access_token (используем внутренний адрес Canvas для backend)
        token_resp = requests.post(
            f"{CANVAS_INTERNAL_DOMAIN}/login/oauth2/token",
            data={
                "grant_type": "authorization_code",
                "client_id": CANVAS_CLIENT_ID,
                "client_secret": CANVAS_CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "code": code
            }
        )
        print("Token response status:", token_resp.status_code)
        print("Token response text:", token_resp.text)

        if token_resp.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Ошибка получения токена: {token_resp.text}")

        token_data = token_resp.json()
        access_token = token_data.get("access_token")
        if not access_token:
            print("Access token отсутствует в ответе:", token_data)
            raise HTTPException(status_code=400, detail="Canvas OAuth2 авторизация не удалась")

        # Получение профиля (используем внутренний адрес Canvas для backend)
        profile_resp = requests.get(
            f"{CANVAS_INTERNAL_DOMAIN}/api/v1/users/self/profile",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        print("Profile response status:", profile_resp.status_code)
        print("Profile response text:", profile_resp.text)

        if profile_resp.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Ошибка получения профиля: {profile_resp.text}")

        canvas_user = profile_resp.json()
        canvas_email = canvas_user.get("primary_email") or canvas_user.get("login_id")
        print("Canvas email:", canvas_email)

        # Поиск или создание пользователя в БД
        user = db.query(models.User).filter(models.User.email == canvas_email).first()
        if not user:
            user = models.User(
                email=canvas_email,
                password_hash=None,
                role=models.UserRole.volunteer,
                first_name=canvas_user.get("name", ""),
                last_name=""
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print("Создан новый пользователь:", user.id)

        # Генерация токена
        token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
        print("JWT token:", token)

        # Сохранение токена
        db_token = db.query(models.Token).filter(models.Token.user_id == user.id).first()
        if db_token:
            db_token.token = token
            db_token.updated_at = datetime.utcnow()
        else:
            db_token = models.Token(user_id=user.id, token=token, is_active=True)
            db.add(db_token)

        db.commit()
        print("Токен сохранён в БД.")

        redirect_url = f"{FRONTEND_SUCCESS_REDIRECT}{token}&canvas_token={access_token}"
        print("Редирект на фронт:", redirect_url)
        return RedirectResponse(url=redirect_url)

    except Exception as e:
        print("‼️ Ошибка в /canvas/callback:")
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"detail": "Ошибка авторизации", "error": str(e)})
    

@router.get("/logout")
def logout_redirect():
    frontend_redirect = "http://localhost:5173/login"
    canvas_logout = f"{CANVAS_EXTERNAL_DOMAIN}/logout?return_to={urllib.parse.quote(frontend_redirect)}"
    return RedirectResponse(canvas_logout)

# @router.get("/login/canvas/force")
# def force_login_canvas():
#     # Сначала выходим из Canvas, потом переходим на login_canvas
#     canvas_logout_url = (
#         f"{CANVAS_EXTERNAL_DOMAIN}/logout?"
#         f"return_to={urllib.parse.quote('http://localhost:8000/api/auth/login/canvas')}"
#     )
#     print("➡️ Принудительный logout в Canvas")
#     return RedirectResponse(canvas_logout_url)
