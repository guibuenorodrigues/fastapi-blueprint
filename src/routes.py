from fastapi import FastAPI

from src.api import v1 as api_v1


def setup(app: FastAPI) -> None:
    """Setup API Routes."""

    api_v1.add_routes(app)
