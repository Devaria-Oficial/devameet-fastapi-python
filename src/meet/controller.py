from fastapi import APIRouter, Depends

from src.auth.handler import get_current_user

from .schema import CreateMeet
from .service import MeetService


router = APIRouter()

@router.post('/')
async def create_meet(create_meet_dto: CreateMeet, service: MeetService = Depends(MeetService), username: str = Depends(get_current_user)):
    return service.create_meet(create_meet_dto)