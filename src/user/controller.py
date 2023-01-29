from fastapi import APIRouter, Depends

from src.auth.handler import get_current_user

from .service import UserService


router = APIRouter()

@router.get('/')
async def read_users_me(username: str = Depends(get_current_user), service: UserService = Depends(UserService)):
    return service.get_user_by_username(username)