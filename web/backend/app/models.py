from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Table d'association pour la relation many-to-many entre Profile et Competency
profile_competency = Table('profile_competency', Base.metadata,
    Column('profile_id', Integer, ForeignKey('profiles.id'), primary_key=True),
    Column('competency_id', Integer, ForeignKey('competencies.id'), primary_key=True)
)

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    competencies = relationship("Competency", secondary=profile_competency, back_populates="profiles")

class Competency(Base):
    __tablename__ = "competencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    level = Column(Integer)
    description = Column(String, nullable=True)
    profiles = relationship("Profile", secondary=profile_competency, back_populates="competencies") 