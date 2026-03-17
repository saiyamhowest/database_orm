from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from models.birds import Bird

class Birdspotting(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bird_id: int = Field(foreign_key="birds.id")
    spotted_at: datetime
    location: str
    observer_name: str
    notes: Optional[str]

    bird: Optional[Bird] = Relationship()