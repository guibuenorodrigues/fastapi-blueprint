# app/api/middleware/request_logging.py

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# Configure a logger for requests
request_logger = logging.getLogger("api.requests")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        Logs incoming request details and response status/duration.
        """
        start_time = time.time()
        # Log request details (path, method, client IP)
        request_logger.info(f"Request: {request.method} {request.url.path} from {request.client.host}")

        response = await call_next(request)

        process_time = time.time() - start_time
        # Log response details (status code, processing time)
        request_logger.info(
            f"Response: {request.method} {request.url.path} Status: {response.status_code} Took: {process_time:.4f}s"
        )
        return response


# To add to FastAPI app in main.py:
# from app.api.middleware.request_logging import RequestLoggingMiddleware
# app.add_middleware(RequestLoggingMiddleware)
