from typing import Annotated

from httpx import ASGITransport, AsyncClient
from pytest_asyncio import fixture as async_fixture

from src.main import app


@async_fixture(scope="module")
async def http_client() -> AsyncClient:
    """
    Fixture that provides an asynchronous test client for the FastAPI app.
    The scope="module" ensures the client is created once per module of tests.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


HTTPCLient = Annotated[AsyncClient, http_client]
