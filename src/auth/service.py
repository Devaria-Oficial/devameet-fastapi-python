from fastapi import HTTPException
from .schema import Login


class AuthService:
    def login(self, user: Login):
        if not (user.login == 'teste@teste.com' and user.password == '123456'):
            raise HTTPException(400, 'Invalid login or password')
        
        return {'message': 'Logged in'}