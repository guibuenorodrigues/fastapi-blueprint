import pytest

from tests.conftest import HTTPCLient


@pytest.mark.asyncio
async def test_healthz_endpoint_healthy(http_client: HTTPCLient):
    """Test the /healthz endpoint when all dependencies are healthy."""

    response = await http_client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {}


# import pytest
# from httpx import AsyncClient
# from unittest.mock import AsyncMock

# # Import your FastAPI app and the dependency to be mocked
# from src.main import app
# from src.api.v1.endpoints import healthz as healthz_module


# @pytest.mark.asyncio
# async def test_healthz_endpoint_healthy(mocker):
#     """
#     Test the /healthz endpoint when all dependencies are healthy.
#     Mocks the check_db_connection dependency to return True.
#     """
#     # Use pytest-mock's mocker to patch the dependency
#     # We patch the dependency in the module where it's *used*, not where it's defined
#     mock_db_check = mocker.patch(
#         "src.api.v1.endpoints.healthz.check_db_connection",
#         new_callable=AsyncMock
#     )
#     mock_db_check.return_value = True # Simulate a healthy DB connection

#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.get("/healthz")

#     assert response.status_code == 200
#     assert response.json() == {"status": "ok", "message": "Service is healthy"}
#     mock_db_check.assert_called_once() # Ensure our mock was called
