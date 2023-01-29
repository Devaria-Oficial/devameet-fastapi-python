from fastapi import APIRouter, Body, Depends

from src.auth.handler import get_current_user

from .schema import UpdateUser
from .service import UserService


router = APIRouter()

@router.get('/')
async def read_users_me(username: str = Depends(get_current_user), service: UserService = Depends(UserService)):
    return service.get_user_by_username(username)

@router.put('/{id}')
async def update_user(
    id: str, 
    user_data: UpdateUser = Body(embed=False), 
    username: str = Depends(get_current_user), 
    service: UserService = Depends(UserService)):
    return service.update_user(id, username, user_data)