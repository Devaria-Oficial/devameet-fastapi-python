from fastapi import Depends, FastAPI
from .core import config
from .core.router import router


def build_api() -> FastAPI:
    application = FastAPI()

    application.include_router(router, prefix="/api")

    return application

app = build_api()