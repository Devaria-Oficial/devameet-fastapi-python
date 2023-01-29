from pydantic import BaseModel, EmailStr, Field


class CreateMeet(BaseModel):
    name: str = Field(..., min_length=2)
    color: str = Field(..., regex='[0-9A-Fa-f]{6}')