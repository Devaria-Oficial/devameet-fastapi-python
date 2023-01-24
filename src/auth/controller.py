from fastapi import APIRouter

from .service import AuthService
from .schema import Login

router = APIRouter()

@router.post('/login')
async def login(user: Login):
    service = AuthService()
    return service.login(user)