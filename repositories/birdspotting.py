from sqlmodel import Session, select
from models.birdspotting import Birdspotting

class BirdspottingRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.exec(select(Birdspotting)).all()

    def get_one(self, id: int):
        return self.session.get(Birdspotting, id)

    def insert(self, data: Birdspotting):
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data