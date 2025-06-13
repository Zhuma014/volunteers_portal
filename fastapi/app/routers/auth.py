from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import SessionLocal
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from app.dependencies import get_db

# Настройки JWT (секрет и алгоритм)
SECRET_KEY = "your_super_secret_key"  # Поменяй на свой и не хранить в коде в реальных проектах
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 день

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=["auth"])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=60))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=schemas.UserResponse)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # Проверяем уникальность iin
    user = db.query(models.User).filter(models.User.iin == user_in.iin).first()
    if user:
        raise HTTPException(status_code=400, detail="Пользователь с таким ИИН уже существует")
    
    # Проверка по номеру телефона, если он есть
    if user_in.phone_number:
        phone_user = db.query(models.User).filter(models.User.phone_number == user_in.phone_number).first()
        if phone_user:
            raise HTTPException(status_code=400, detail="Пользователь с таким номером телефона уже существует")

    # Хэшируем пароль
    hashed_password = get_password_hash(user_in.password)

    # Создаем пользователя с именем и фамилией
    user = models.User(
        iin=user_in.iin,
        phone_number=user_in.phone_number,
        password_hash=hashed_password,
        role=user_in.role or models.UserRole.volunteer,
        first_name=user_in.first_name,
        last_name=user_in.last_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login")
def login(user_in: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.iin == user_in.iin).first()
    if not user or not verify_password(user_in.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Неверный ИИН или пароль")

    new_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})

    existing_token = db.query(models.Token).filter(
        models.Token.user_id == user.id,
        models.Token.is_active == True
    ).first()

    if existing_token:
        existing_token.token = new_token
        existing_token.updated_at = datetime.utcnow()
    else:
        db_token = models.Token(
            user_id=user.id,
            token=new_token,
            is_active=True
        )
        db.add(db_token)

    db.commit()
    return {"access_token": new_token, "token_type": "bearer"}



