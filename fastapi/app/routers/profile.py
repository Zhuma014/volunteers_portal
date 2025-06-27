from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserResponse, UserUpdate
from app.dependencies import get_db, get_current_user
from passlib.context import CryptContext

router = APIRouter(tags=["profile"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@router.get("/profile", response_model=UserResponse)
def read_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/profile/{user_id}", response_model=UserResponse)
def get_profile_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/profile", response_model=UserResponse)
def update_profile(update_data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        if update_data.password:
            current_user.hashed_password = hash_password(update_data.password)  # обязательно хешировать
        else:
            raise HTTPException(status_code=400, detail="Пароль обязателен для обновления")
        
        db.commit()
        db.refresh(current_user)
        return current_user
    except Exception as e:
        print(f"Update error: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong")