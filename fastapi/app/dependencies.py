# app/dependencies.py

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from app.database import SessionLocal
from app import models

# Используется и для логина через email, и для Canvas OAuth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Важно: секрет лучше вынести в .env файл
SECRET_KEY = "your_super_secret_key"
ALGORITHM = "HS256"

# Получение сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Получение текущего пользователя по JWT-токену (используется и после Canvas login)
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Проверка, что токен активен
    token_entry = db.query(models.Token).filter_by(token=token, is_active=True).first()
    if not token_entry:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user
