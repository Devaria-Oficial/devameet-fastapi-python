from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    log_level: str = "info"
    db_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 3600

    class Config:
        env_file = '.env'

@lru_cache()
def get_settings():
    return Settings()