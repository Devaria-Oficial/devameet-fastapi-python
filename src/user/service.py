from fastapi import Depends
from src.core.middleware.error import ApiError
from src.auth.model import User
from src.core.database import SessionLocal, get_db

from .schema import UpdateUser


class UserService:
    def __init__(self, db: SessionLocal = Depends(get_db)):
        self.db = db

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def update_user(self, user_id : str, username: str, update_user_dto: UpdateUser):
        user = self.db.query(User).filter(User.id == user_id, User.username == username).first()
        if not user:
            raise ApiError(message="Cannot update this user", error="Bad Request", status_code=400)

        user.name = update_user_dto.name
        user.avatar = update_user_dto.avatar
        self.db.commit()
        self.db.refresh(user)

        return user