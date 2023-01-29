from datetime import timedelta, datetime
from fastapi import Depends
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

from src.core.middleware.error import ApiError
from src.core.config import get_settings

config = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Authorization")

class TokenHandler:
    @staticmethod
    def create_access_token(username: str):
        expire = datetime.utcnow() + timedelta(seconds=config.jwt_expiration)
        data = {"sub": username, "exp": expire}
        encoded_jwt = jwt.encode(data, config.jwt_secret, algorithm=config.jwt_algorithm)
        return encoded_jwt

    @staticmethod
    def read_token(token: str):
        try:
            payload = jwt.decode(token, config.jwt_secret, algorithms=[config.jwt_algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise ApiError(message="Invalid token", error="Invalid token", status_code=401)
            return username
        except JWTError:
            raise ApiError(message="Invalid token", error="Invalid token", status_code=401)

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = TokenHandler.read_token(token)
    return username