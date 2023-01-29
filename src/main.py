from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException

from .core.middleware.error import ErrorConverterMiddleware, ErrorHandlerMiddleware, handle_http_exception, handle_validation_error
from .core.middleware.database_session_middleware import DatabaseSessionMiddleware
from .core.router import router

def build_api() -> FastAPI:
    application = FastAPI()

    application.add_exception_handler(RequestValidationError, handle_validation_error)
    application.add_exception_handler(HTTPException, handle_http_exception)

    application.add_middleware(DatabaseSessionMiddleware)
    application.add_middleware(ErrorConverterMiddleware)
    application.add_middleware(ErrorHandlerMiddleware)

    application.include_router(router, prefix="/api")

    return application

app = build_api()