from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from app.dependencies import get_db

router = APIRouter(tags=["meta"])


@router.get("/regions", response_model=List[schemas.RegionSchema])
def get_regions(db: Session = Depends(get_db)):
    return db.query(models.Region).all()


@router.get("/regions/{region_id}", response_model=schemas.RegionSchema)
def get_region_by_id(region_id: int, db: Session = Depends(get_db)):
    region = db.query(models.Region).filter(models.Region.id == region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="Регион не найден")
    return region


@router.get("/cities", response_model=List[schemas.CitySchema])
def get_cities(region_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    if region_id is not None:
        cities = db.query(models.City).filter(models.City.region_id == region_id).all()
    else:
        cities = db.query(models.City).all()

    if not cities:
        raise HTTPException(status_code=404, detail="Города не найдены")

    return cities


@router.get("/cities/{city_id}", response_model=schemas.CitySchema)
def get_city_by_id(city_id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="Город не найден")
    return city


@router.get("/categories", response_model=List[schemas.CategorySchema])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()


@router.get("/categories/{category_id}", response_model=schemas.CategorySchema)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category