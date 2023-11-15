import os
from unittest import mock

from httpx import AsyncClient

from src.main import app
from tests.fixture import (
    auth_service_response,
    chat_gpt_response,
    create_tpi_fix,
    data,
    headers,
    headers_bad,
    mock_response,
    mock_response_bad,
    response_api,
)

client = AsyncClient(app=app)


async def test_create_tpi():
    with mock.patch(
        "src.handlers.router.request_auth_create_tpi",
    ) as mock_create_tpi:
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
    with mock.patch(
        "src.handlers.router.request_auth_create_tpi",
    ) as mock_bad_create_tpi:
        mock_bad_create_tpi.return_value = mock_response_bad
        result = await client.post(
            url=os.getenv("TEST_URL_CREATE_TPI"),
            json=create_tpi_fix,
            headers=headers_bad,
        )
        assert result.status_code == 403
        assert result.json() == mock_response_bad["message"]
        assert mock_bad_create_tpi.call_count == 1


async def test_bad_create_tpi_without_headers():
    result = await client.post(
        url=os.getenv("TEST_URL_CREATE_TPI"),
        json=create_tpi_fix,
    )
    assert result.status_code == 401
    assert result.json() == {
        "message": "provide an access token",
    }


async def test_get_road_data():
    mock_send_header_to_auth_service = mock.AsyncMock(
        return_value=auth_service_response
    )
    mock_get_weather = mock.AsyncMock(return_value=response_api)
    mock_chatgpt = mock.AsyncMock(return_value=chat_gpt_response)
    with mock.patch(
        "src.handlers.router.send_header_to_auth_service",
        mock_send_header_to_auth_service,
    ), mock.patch(
        "src.handlers.router.processed_data_weather", mock_get_weather
    ), mock.patch(
        "src.handlers.router.response_openai", mock_chatgpt
    ):
        query_params = {
            "lat": data["lat"],
            "lon": data["lon"],
        }
        result = await client.get(
            url=os.getenv("TEST_URL_TRAFFIC"),
            params=query_params,
            headers=headers,
        )
        assert result.status_code == 200
        assert result.json()["message"] == chat_gpt_response["message"]


async def test_get_road_data_failure():
    auth_service_response_failure = {
        "status": 401,
        "message": "Token is invalid",
    }
    mock_token_verification = mock.AsyncMock(return_value=auth_service_response_failure)
    with mock.patch(
        "src.handlers.router.send_header_to_auth_service", mock_token_verification
    ):
        query_params = {
            "lat": data["lat"],
            "lon": data["lon"],
        }
        result = await client.get(
            url=os.getenv("TEST_URL_TRAFFIC"),
            params=query_params,
            headers=headers,
        )
        assert result.status_code == 401
        assert result.json() == "Token is invalid"


async def test_get_road_data_without_headers():
    query_params = {
        "lat": data["lat"],
        "lon": data["lon"],
    }
    result = await client.get(
        url=os.getenv("TEST_URL_TRAFFIC"),
        params=query_params,
    )
    assert result.status_code == 401
    assert result.json()["message"] == "provide an access token"


async def test_get_road_data_without_query_params():
    query_params = {
        "lat": None,
        "lon": None,
    }
    result = await client.get(
        url=os.getenv("TEST_URL_TRAFFIC"),
        params=query_params,
    )
    assert result.status_code == 422


async def test_get_road_data_without_response_chatgpt():
    chat_gpt_response_bad = None
    mock_send_header_to_auth_service = mock.AsyncMock(
        return_value=auth_service_response
    )
    mock_get_weather = mock.AsyncMock(return_value=response_api)
    mock_chatgpt = mock.AsyncMock(return_value=chat_gpt_response_bad)
    with mock.patch(
        "src.handlers.router.send_header_to_auth_service",
        mock_send_header_to_auth_service,
    ), mock.patch(
        "src.handlers.router.processed_data_weather", mock_get_weather
    ), mock.patch(
        "src.handlers.router.response_openai", mock_chatgpt
    ):
        query_params = {
            "lat": data["lat"],
            "lon": data["lon"],
        }
        result = await client.get(
            url=os.getenv("TEST_URL_TRAFFIC"),
            params=query_params,
            headers=headers,
        )
        assert result.status_code == 200
        assert result.json() == response_api
