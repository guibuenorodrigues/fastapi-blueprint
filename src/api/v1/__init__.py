from fastapi import FastAPI

from .endpoints import healthz


def add_routes(app: FastAPI) -> None:
    app.include_router(healthz.router, prefix="/v1")
