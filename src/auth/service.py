from fastapi import HTTPException
from passlib.context import CryptContext

from sqlalchemy.orm import Session

from .schema import Login, Register
from .model import User


class AuthService:
    def __init__(self, db: Session):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.db = db

    def login(self, user: Login):
        if not (user.login == 'teste@teste.com' and user.password == '123456'):
            raise HTTPException(400, 'Invalid login or password')
        
        return {'message': 'Logged in'}

    def register(self, register_dto: Register):
        hashed_password = self.pwd_context.hash(secret=register_dto.password)
        
        user = User(
            name=register_dto.name,
            avatar=register_dto.avatar,
            username=register_dto.email,
            hashed_password=hashed_password,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user