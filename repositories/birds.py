from sqlmodel import Session, select
from models.birds import Bird, BirdCreate
from models.species import Species

class BirdRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.exec(select(Bird)).all()

    def insert(self, data: BirdCreate):
        species = self.session.get(Species, data.species_id)

        if not species:
            raise ValueError("Species not found")

        obj = Bird.model_validate(data)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj