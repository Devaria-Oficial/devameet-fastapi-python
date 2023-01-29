from fastapi import Depends
from src.auth.model import User
from src.core.database import SessionLocal, get_db


class UserService:
    def __init__(self, db: SessionLocal = Depends(get_db)):
        self.db = db

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()