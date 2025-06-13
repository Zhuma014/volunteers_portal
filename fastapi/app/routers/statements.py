from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter(tags=["Statements"])

@router.get("/organizations", response_model=List[schemas.OrganizationResponse])
def get_organizations(db: Session = Depends(get_db)):
    return db.query(models.Organization).all()


@router.get("/statements", response_model=List[schemas.StatementResponse])
def get_my_statements(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Statement).filter_by(owner_id=current_user.id).all()


@router.post("/statements", response_model=schemas.StatementResponse)
def send_statement(
    statement_in: schemas.StatementCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    case = db.query(models.Case).filter_by(id=statement_in.case_id, owner_id=current_user.id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Жалоба не найдена или не принадлежит вам")

    statement = models.Statement(
        case_id=statement_in.case_id,
        owner_id=current_user.id,
        content=statement_in.content
    )
    db.add(statement)
    db.commit()
    db.refresh(statement)
    return statement
