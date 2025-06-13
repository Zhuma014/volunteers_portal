from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user
from app import models, schemas
from app.models import CaseStatus, UserRole

router = APIRouter(tags=["Staff Cases"])


@router.get("/staff/cases", response_model=List[schemas.CaseResponse])
def get_all_cases(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != UserRole.antikor_staff:
        raise HTTPException(status_code=403, detail="Нет доступа")
    return db.query(models.Case).all()


@router.get("/staff/cases/{case_id}", response_model=schemas.CaseResponse)
def get_case_detail(case_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != UserRole.antikor_staff:
        raise HTTPException(status_code=403, detail="Нет доступа")

    case = db.query(models.Case).filter_by(id=case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Жалоба не найдена")
    return case


@router.patch("/staff/cases/{case_id}/status", response_model=schemas.CaseResponse)
def update_case_status(case_id: int, status: CaseStatus, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != UserRole.antikor_staff:
        raise HTTPException(status_code=403, detail="Нет доступа")

    case = db.query(models.Case).filter_by(id=case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Жалоба не найдена")

    case.status = status
    db.commit()
    db.refresh(case)
    return case


@router.post("/staff/cases/{case_id}/feedback")
def send_feedback(case_id: int, feedback_in: schemas.FeedbackCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != UserRole.antikor_staff:
        raise HTTPException(status_code=403, detail="Нет доступа")

    case = db.query(models.Case).filter_by(id=case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Жалоба не найдена")

    feedback = models.Feedback(
        message=feedback_in.message,
        case_id=case_id,
        staff_id=current_user.id
    )
    db.add(feedback)
    db.commit()
    return {"message": "Обратная связь отправлена"}
