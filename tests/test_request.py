import os
from http import HTTPStatus
from unittest import mock
from unittest.mock import MagicMock, patch

from httpx import AsyncClient
from starlette import status

from src.auth.check_auth import send_header_to_auth_service
from src.auth.crud_tpi import request_auth_create_tpi
from src.main import app
from tests.fixture import create_tpi_fix, data, headers, headers_bad

client = AsyncClient(app=app)


@patch("src.auth.check_auth.requests")
async def test_send_header_to_auth_service(mock_requests):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": "created",
        "status": 201,
    }
    mock_requests.post.return_value = mock_response
    response = await send_header_to_auth_service(headers)
    assert response["status"] == HTTPStatus.OK
    assert response["message"] == {
        "message": "created",
        "status": 201,
    }


@patch("src.auth.crud_tpi.requests")
async def test_request_auth_create_tpi(mock_requests):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "message": "tpi created successfully",
    }
    mock_requests.post.return_value = mock_response
    response = await request_auth_create_tpi(
        data["lat"],
        data["lon"],
        "Volgograd",
        headers,
    )
    assert response["status"] == HTTPStatus.CREATED
    assert response["message"] == {
        "message": "tpi created successfully",
    }


async def test_create_tpi():
    mock_response = {
        "message": {
            "latitude": 55.0,
            "longitude": 37.0,
            "direction": "Вологда-Москва",
        },
        "status": status.HTTP_201_CREATED,
    }
    with mock.patch("src.handlers.router.request_auth_create_tpi") as mock_create_tpi:
        mock_create_tpi.return_value = mock_response
        result = await client.post(
            url=os.getenv("TEST_URL_CREATE_TPI"),
            json=create_tpi_fix,
            headers=headers,
        )
        assert result.status_code == 201
        assert result.json() == mock_response["message"]
        assert mock_create_tpi.call_count == 1


async def test_bad_create_tpi():
    mock_response_bad = {
        "message": {
            "detail": "Недействительный токен доступа",
        },
        "status": status.HTTP_403_FORBIDDEN,
    }
    with mock.patch(
        "src.handlers.router.request_auth_create_tpi",
    ) as mock_non_create_tpi:
        mock_non_create_tpi.return_value = mock_response_bad
        result = await client.post(
            url=os.getenv("TEST_URL_CREATE_TPI"),
            json=create_tpi_fix,
            headers=headers_bad,
        )
        assert result.status_code == 403
        assert result.json() == mock_response_bad["message"]
        assert mock_non_create_tpi.call_count == 1
