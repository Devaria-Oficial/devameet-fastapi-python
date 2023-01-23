from fastapi import Depends, FastAPI
from .core import config

app = FastAPI()


@app.get("/")
async def root(settings: config.Settings = Depends(config.get_settings)):
    return {"LOG_LEVEL": settings.log_level}