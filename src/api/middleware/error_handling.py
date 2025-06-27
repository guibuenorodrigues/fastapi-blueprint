# app/api/middleware/error_handling.py

import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from src.core.exceptions import CustomException  # Your custom base exception

error_logger = logging.getLogger("api.errors")


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except CustomException as e:
            # Handle your custom application exceptions
            error_logger.warning(f"Custom error for {request.url.path}: {e.detail}", exc_info=True)
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail, "code": e.code},  # Custom error codes
            )
        except Exception as e:
            # Catch all other unexpected exceptions
            error_logger.exception(f"Unhandled exception for {request.url.path}: {e}")
            return JSONResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "An unexpected error occurred. Please try again later.", "code": "SERVER_ERROR"},
            )


# To add to FastAPI app in main.py:
# from app.api.middleware.error_handling import ErrorHandlingMiddleware
# app.add_middleware(ErrorHandlingMiddleware)
