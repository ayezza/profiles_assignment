from pydantic import BaseModel
from typing import List, Optional

class CompetencyBase(BaseModel):
    name: str
    level: int
    description: Optional[str] = None

class CompetencyCreate(CompetencyBase):
    pass

class Competency(CompetencyBase):
    id: int
    
    class Config:
        from_attributes = True

class ProfileBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProfileCreate(ProfileBase):
    competency_ids: List[int] = []

class Profile(ProfileBase):
    id: int
    competencies: List[Competency] = []
    
    class Config:
        from_attributes = True 