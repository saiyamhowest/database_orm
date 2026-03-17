from sqlmodel import Session, select
from models.species import Species, SpeciesCreate

class SpeciesRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.exec(select(Species)).all()

    def insert(self, data: SpeciesCreate):
        obj = Species.model_validate(data)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj