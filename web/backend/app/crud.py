from sqlalchemy.orm import Session
from . import models, schemas

def get_profile(db: Session, profile_id: int):
    return db.query(models.Profile).filter(models.Profile.id == profile_id).first()

def get_profiles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Profile).offset(skip).limit(limit).all()

def create_profile(db: Session, profile: schemas.ProfileCreate):
    db_profile = models.Profile(name=profile.name, description=profile.description)
    if profile.competency_ids:
        competencies = db.query(models.Competency).filter(models.Competency.id.in_(profile.competency_ids)).all()
        db_profile.competencies = competencies
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_competency(db: Session, competency_id: int):
    return db.query(models.Competency).filter(models.Competency.id == competency_id).first()

def get_competencies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Competency).offset(skip).limit(limit).all()

def create_competency(db: Session, competency: schemas.CompetencyCreate):
    db_competency = models.Competency(**competency.dict())
    db.add(db_competency)
    db.commit()
    db.refresh(db_competency)
    return db_competency 