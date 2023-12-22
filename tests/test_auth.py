from unittest.mock import Mock, patch

from starlette import status

from src.auth.check_auth import send_header_to_auth_service
from src.auth.crud_tpi import request_auth_create_tpi
from tests.fixture import headers, request_tpi_schemas


@patch("src.auth.crud_tpi.requests")
async def test_request_auth_create_tpi(mock_requests):
    mock_requests.post.return_value.status_code = status.HTTP_201_CREATED
    response = await request_auth_create_tpi(
        request_tpi_schemas, headers["Authorization"], 55.02, 22.201
    )
    assert response is True


@patch("src.auth.crud_tpi.requests")
async def test_request_auth_create_tpi_bad(mock_requests):
    mock_requests.post.return_value.status_code = status.HTTP_401_UNAUTHORIZED
    response = await request_auth_create_tpi(
        request_tpi_schemas, headers["Authorization"], 55.02, 22.201
    )
    assert response is False


@patch("src.auth.check_auth.requests")
async def test_send_header_to_auth_service(mock_requests):
    mock_response = {"lat_end": 55.37, "lon_end": 58.25}
    mock_requests.get.return_value.status_code = status.HTTP_200_OK
    mock_requests.get.return_value.json = Mock(return_value=mock_response)
    response = await send_header_to_auth_service(headers, request_tpi_schemas)
    assert response == {"lat_end": 55.37, "lon_end": 58.25}
