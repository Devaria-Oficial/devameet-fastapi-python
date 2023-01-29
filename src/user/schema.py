from pydantic import BaseModel

class UpdateUser(BaseModel):
    name: str
    avatar: str