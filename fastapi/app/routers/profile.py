from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserResponse, UserUpdate
from app.dependencies import get_db, get_current_user

router = APIRouter(tags=["profile"])

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
        if update_data.phone_number:
            current_user.phone_number = update_data.phone_number
        if update_data.role:
            current_user.role = update_data.role
        db.commit()
        db.refresh(current_user)
        return current_user
    except Exception as e:
        print(f"Update error: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong")