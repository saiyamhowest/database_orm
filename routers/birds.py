from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import Session
from database import get_session
from repositories.birds import BirdRepository
from models.birds import Bird, BirdCreate

router = APIRouter(prefix="/birds", tags=["Birds"])

def get_repo(session: Session = Depends(get_session)):
    return BirdRepository(session)

@router.get("/", response_model=List[Bird])
def get_all(repo: BirdRepository = Depends(get_repo)):
    return repo.get_all()

@router.post("/", response_model=Bird)
def create(data: BirdCreate, repo: BirdRepository = Depends(get_repo)):
    return repo.insert(data)