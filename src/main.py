from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
    )

    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(RequestLoggingMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    routes.setup(app)

    return app


app = create_app()
