from fastapi import Depends
from src.core.database import SessionLocal, get_db

from .model import Meet
from .schema import CreateMeet, UpdateMeet


class MeetService:
    def __init__(self, db: SessionLocal = Depends(get_db)):
        self.db = db

    def create_meet(self, create_meet_dto: CreateMeet):
        meet = Meet(name=create_meet_dto.name, color=create_meet_dto.color)

        self.db.add(meet)
        self.db.commit()
        self.db.refresh(meet)
        return meet

    def get_all_meets(self):
        return self.db.query(Meet).all()

    def update_meet(self, id: str, update_meet_dto: UpdateMeet):
        meet = self.db.query(Meet).filter(Meet.id == id).one()
        
        meet.name = update_meet_dto.name
        meet.color = update_meet_dto.color
        
        self.db.commit()
        self.db.refresh(meet)

        return meet