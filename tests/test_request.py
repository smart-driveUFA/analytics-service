import os
from unittest import mock

from httpx import AsyncClient

from src.main import app
from tests.fixture import (
    auth_service_response,
    chat_gpt_response,
    create_tpi_fix,
    headers,
    headers_bad,
    response_api,
    start_data,
    stop_data,
    traffic_jams_good,
)

client = AsyncClient(app=app)


async def test_create_tpi():
    with mock.patch(
        "src.handlers.router.request_auth_create_tpi",
    ) as mock_create_tpi:
        mock_create_tpi.return_value = True
        result = await client.post(
            url=os.getenv("TEST_URL_CREATE_TPI"),
            json=create_tpi_fix,
            headers=headers,
        )
        assert result.status_code == 201
        assert result.json() == {
            "message": "successfully added",
        }
        assert mock_create_tpi.call_count == 1


async def test_bad_create_tpi():
    with mock.patch(
        "src.handlers.router.request_auth_create_tpi",
    ) as mock_bad_create_tpi:
        mock_bad_create_tpi.return_value = False
        result = await client.post(
            url=os.getenv("TEST_URL_CREATE_TPI"),
            json=create_tpi_fix,
            headers=headers_bad,
        )
        assert result.status_code == 401
        assert result.json() == {
            "message": "token is invalid",
        }
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


async def test_collect_road_data():
    mock_send_header_to_auth_service = mock.AsyncMock(
        return_value=auth_service_response,
    )
    mock_return_summing_result_road = mock.AsyncMock(
        return_value={
            "weather": response_api,
            "recommended information": chat_gpt_response["message"],
            "road_traffic_status": traffic_jams_good,
        }
    )
    with mock.patch(
        "src.handlers.router.send_header_to_auth_service",
        mock_send_header_to_auth_service,
    ), mock.patch(
        "src.handlers.router.summing_result_road", mock_return_summing_result_road
    ):
        query_params = {
            "start": {
                "lat": start_data["lat"],
                "lon": start_data["lon"],
            },
            "stop": {
                "lat": stop_data["lat"],
                "lon": stop_data["lon"],
            },
        }
        result = await client.post(
            url=os.getenv("TEST_URL_TRAFFIC"),
            json=query_params,
            headers=headers,
        )
        assert result.status_code == 200
        assert result.json() == {
            "weather": response_api,
            "recommended information": chat_gpt_response["message"],
            "road_traffic_status": traffic_jams_good,
        }


async def test_collect_road_data_failure():
    with mock.patch(
        "src.handlers.router.send_header_to_auth_service",
    ) as response_auth:
        response_auth.return_value = False
        query_params = {
            "start": {
                "lat": start_data["lat"],
                "lon": start_data["lon"],
            },
            "stop": {
                "lat": stop_data["lat"],
                "lon": stop_data["lon"],
            },
        }
        result = await client.post(
            url=os.getenv("TEST_URL_TRAFFIC"),
            json=query_params,
            headers=headers,
        )
        assert result.status_code == 401
        assert result.json() == {
            "message": "token is invalid",
        }


async def test_collect_road_data_without_headers():
    query_params = {
        "start": {
            "lat": start_data["lat"],
            "lon": start_data["lon"],
        },
        "stop": {
            "lat": stop_data["lat"],
            "lon": stop_data["lon"],
        },
    }
    result = await client.post(
        url=os.getenv("TEST_URL_TRAFFIC"),
        json=query_params,
    )
    assert result.status_code == 401
    assert result.json()["message"] == "provide an access token"


async def test_collect_road_data_without_query_params():
    result = await client.post(
        url=os.getenv("TEST_URL_TRAFFIC"),
    )
    assert result.status_code == 422
