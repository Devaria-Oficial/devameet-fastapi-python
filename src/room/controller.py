from fastapi import APIRouter, Depends

from src.auth.handler import get_current_user

from .service import RoomService

router = APIRouter()
    
@router.get('/{link}')
async def get_room(link: str, service: RoomService = Depends(RoomService), username: str = Depends(get_current_user)):
    return service.get_room(link)