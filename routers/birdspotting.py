from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import Session
from database import get_session
from repositories.birdspotting import BirdspottingRepository
from models.birdspotting import Birdspotting

router = APIRouter(prefix="/birdspotting", tags=["Birdspotting"])

def get_repo(session: Session = Depends(get_session)):
    return BirdspottingRepository(session)

@router.get("/", response_model=List[Birdspotting])
def get_all(repo: BirdspottingRepository = Depends(get_repo)):
    return repo.get_all()

@router.get("/{id}")
def get_one(id: int, repo: BirdspottingRepository = Depends(get_repo)):
    return repo.get_one(id)

@router.post("/")
def create(data: Birdspotting, repo: BirdspottingRepository = Depends(get_repo)):
    return repo.insert(data)