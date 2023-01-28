from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db

from .service import AuthService
from .schema import Login, Register

router = APIRouter()

@router.post('/login')
async def login(user: Login):
    service = AuthService()
    return service.login(user)


@router.post('/register')
async def register(user: Register, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register(user)