from pydantic import BaseModel, EmailStr, Field


class Login(BaseModel):
    login: str
    password: str

class Register(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=20, regex='((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$')
    name: str = Field(..., min_length=2)
    avatar: str

class Token(BaseModel):
    email: str
    name: str
    token: str