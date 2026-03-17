from typing import Optional
from sqlmodel import SQLModel, Field

class SpeciesBase(SQLModel):
    name: str
    scientific_name: str
    family: str
    conservation_status: str
    wingspan_cm: float

class Species(SpeciesBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class SpeciesCreate(SpeciesBase):
    pass