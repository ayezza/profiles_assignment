from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import get_db

router = APIRouter()

@router.post("/profiles/", response_model=schemas.Profile)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    return crud.create_profile(db=db, profile=profile)

@router.get("/profiles/", response_model=List[schemas.Profile])
def read_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    profiles = crud.get_profiles(db, skip=skip, limit=limit)
    return profiles

@router.get("/profiles/{profile_id}", response_model=schemas.Profile)
def read_profile(profile_id: int, db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile non trouvé")
    return db_profile

@router.post("/competencies/", response_model=schemas.Competency)
def create_competency(competency: schemas.CompetencyCreate, db: Session = Depends(get_db)):
    return crud.create_competency(db=db, competency=competency)

@router.get("/competencies/", response_model=List[schemas.Competency])
def read_competencies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    competencies = crud.get_competencies(db, skip=skip, limit=limit)
    return competencies

@router.get("/competencies/{competency_id}", response_model=schemas.Competency)
def read_competency(competency_id: int, db: Session = Depends(get_db)):
    db_competency = crud.get_competency(db, competency_id=competency_id)
    if db_competency is None:
        raise HTTPException(status_code=404, detail="Compétence non trouvée")
    return db_competency 