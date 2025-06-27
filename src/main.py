from fastapi import FastAPI

from src import routes
from src.api.middleware.error_handling import ErrorHandlingMiddleware
from src.api.middleware.request_logging import RequestLoggingMiddleware
from src.core.config import settings
from src.core.logging import setup_logging

# setup logging settings
setup_logging()


def create_app() -> FastAPI:
    """Create FastAPI APP."""

    # setup FastAPI
    app = FastAPI(
        title=settings.NAME,
        debug=settings.DEBUG,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
    )

    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(RequestLoggingMiddleware)

    routes.setup(app)

    return app


app = create_app()
