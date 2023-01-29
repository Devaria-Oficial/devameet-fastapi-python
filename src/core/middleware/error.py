import traceback

import sqlalchemy.exc
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse


class ApiError(Exception):
    def __init__(self, message, error, status_code=500):
        self.message = message
        self.error = error
        self.status_code = status_code

    def __str__(self):
        return self.message


class ErrorConverterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            response = await call_next(request)
        except Exception as e:
            traceback.print_exc()

            if isinstance(e, ApiError):
                raise

            error_dict = {
                404: "Item Not Found",
                500: "Internal Server Error",
            }

            message = str(e)
            status_code = 500

            if isinstance(e, sqlalchemy.exc.NoResultFound):
                status_code = 404

            raise ApiError(message=message, error=error_dict[status_code], status_code=status_code)
        return response

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            response = await call_next(request)
        except ApiError as e:
            response = JSONResponse(
                status_code=e.status_code,
                content={
                    "message": e.message.split(";"),
                    "error": e.error,
                    "statusCode": e.status_code
                }
            )
        return response


def handle_http_exception(request: Request, exc: HTTPException):
    raise ApiError(message=exc.detail, error=exc.detail, status_code=exc.status_code)

def handle_validation_error(request: Request, exc: RequestValidationError):
    errors = ';'.join(get_error_message(err) for err in exc.errors())
    raise ApiError(message=errors, error="Unprocessable Entity", status_code=422)

def get_error_message(error):
    if error['type'] == 'value_error.missing':
        return f"Missing value for {error['loc'][-1]}"
    else:
        header = error['loc'][-1].capitalize()
        return f"{header}: {error['msg']}"