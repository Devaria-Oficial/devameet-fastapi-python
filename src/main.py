from fastapi import FastAPI
from .core.router import router

def build_api() -> FastAPI:
    application = FastAPI()

    application.include_router(router, prefix="/api")

    return application

app = build_api()