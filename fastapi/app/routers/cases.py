from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session,joinedload
from typing import List
from app import models, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter( tags=["cases"])

@router.post("/cases", response_model=schemas.CaseResponse)
def create_case(case_in: schemas.CaseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    case = models.Case(**case_in.dict(), owner_id=current_user.id)
    db.add(case)
    db.commit()
    db.refresh(case)
    return case

@router.get("/cases", response_model=List[schemas.CaseResponse])
def get_my_cases(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    cases = (
        db.query(models.Case)
        .options(
            joinedload(models.Case.owner),
            joinedload(models.Case.region),
            joinedload(models.Case.city),
            joinedload(models.Case.category),
        )
        .filter_by(owner_id=current_user.id)
        .all()
    )
    return cases

@router.get("/cases/{case_id}", response_model=schemas.CaseResponse)
def get_case(case_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    case = (
        db.query(models.Case)
        .options(
            joinedload(models.Case.owner),
            joinedload(models.Case.region),
            joinedload(models.Case.city),
            joinedload(models.Case.category),
            joinedload(models.Case.feedbacks)
        )
        .filter_by(id=case_id, owner_id=current_user.id)
        .first()
    )
    if not case:
        raise HTTPException(status_code=404, detail="Жалоба не найдена")
    return case


@router.put("/cases/{case_id}", response_model=schemas.CaseResponse)
def update_case(case_id: int, case_in: schemas.CaseUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    case = db.query(models.Case).filter_by(id=case_id, owner_id=current_user.id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Жалоба не найдена")
    if case.status not in [ models.CaseStatus.submitted]:
        raise HTTPException(status_code=400, detail="Жалобу можно редактировать только в статусе  'submitted'")
    for key, value in case_in.dict(exclude_unset=True).items():
        setattr(case, key, value)
    db.commit()
    db.refresh(case)
    return case

@router.delete("/cases/{case_id}")
def delete_case(case_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    case = db.query(models.Case).filter_by(id=case_id, owner_id=current_user.id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Жалоба не найдена")
    db.delete(case)
    db.commit()
    return {"detail": "Жалоба удалена"}

@router.get("/cases/{case_id}/feedbacks")
def get_case_feedbacks(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Проверяем, что жалоба принадлежит текущему пользователю
    case = db.query(models.Case).filter_by(id=case_id, owner_id=current_user.id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Жалоба не найдена или нет доступа")

    feedbacks = db.query(models.Feedback).filter_by(case_id=case_id).all()
    return feedbacks
