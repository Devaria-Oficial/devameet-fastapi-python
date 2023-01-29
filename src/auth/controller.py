from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db

from .service import AuthService
from .schema import Login, Register

router = APIRouter()

@router.post('/login')
async def login(login_dto: Login, service: AuthService = Depends(AuthService)):
    return service.login(login_dto)


@router.post('/register')
async def register(register_dto: Register, service: AuthService = Depends(AuthService)):
    return service.register(register_dto)