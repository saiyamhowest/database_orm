from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import Session
from database import get_session
from repositories.species import SpeciesRepository
from models.species import Species, SpeciesCreate

router = APIRouter(prefix="/species", tags=["Species"])

def get_repo(session: Session = Depends(get_session)):
    return SpeciesRepository(session)

@router.get("/", response_model=List[Species])
def get_all(repo: SpeciesRepository = Depends(get_repo)):
    return repo.get_all()

@router.post("/", response_model=Species)
def create(data: SpeciesCreate, repo: SpeciesRepository = Depends(get_repo)):
    return repo.insert(data)