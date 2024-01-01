import os
from unittest import mock

from fastapi import status
from httpx import AsyncClient

from tests.fixture import (
    auth_service_response,
    chat_gpt_response,
    headers,
    headers_bad,
    request_tpi_without_schemas,
    response_api,
    traffic_jams_good,
)


async def test_create_tpi(client: AsyncClient):
    with mock.patch(
        "src.handlers.router.request_auth_create_tpi",
    ) as mock_create_tpi, mock.patch(
        "src.handlers.router.find_coordinates_end_of_highway",
    ) as mock_coor_end:
        mock_coor_end.return_value = 37.07, 54.05
        result = await client.post(
            url=os.getenv("TEST_URL_CREATE_TPI"),  # type: ignore[]
            json=request_tpi_without_schemas,
            headers=headers,
        )
        assert result.status_code == 201
        assert result.json() == {
            "message": "successfully created",
        }
        assert mock_create_tpi.call_count == 1


async def test_bad_create_tpi(client: AsyncClient):
    with mock.patch(
        "src.handlers.router.request_auth_create_tpi",
    ) as mock_bad_create_tpi:
        mock_bad_create_tpi.return_value = False
        with mock.patch(
            "src.handlers.router.find_coordinates_end_of_highway",
        ) as mock_coor_end:
            mock_coor_end.return_value = 37.07, 54.05
            result = await client.post(
                url=os.getenv("TEST_URL_CREATE_TPI"),  # type: ignore[]
                json=request_tpi_without_schemas,
                headers=headers_bad,
            )
            assert result.status_code == 401
            assert result.json() == {
                "message": "check Authorization token, and try again",
            }
            assert mock_bad_create_tpi.call_count == 1


async def test_bad_create_tpi_without_headers(client: AsyncClient):
    result = await client.post(
        url=os.getenv("TEST_URL_CREATE_TPI"),  # type: ignore[]
        json=request_tpi_without_schemas,
    )
    assert result.status_code == 401
    assert result.json() == {
        "message": "check Authorization token, and try again",
    }


async def test_collect_road_data(client: AsyncClient):
    mock_send_header_to_auth_service = mock.AsyncMock(
        return_value=auth_service_response,
    )
    mock_return_summing_result_road = mock.AsyncMock(
        return_value={
            "weather": response_api,
            "recommended_information": chat_gpt_response["message"],
            "traffic_jams_status": traffic_jams_good,
        }
    )
    with mock.patch(
        "src.handlers.router.send_header_to_auth_service",
        mock_send_header_to_auth_service,
    ), mock.patch(
        "src.handlers.router.summing_result_road",
        mock_return_summing_result_road,
    ):
        result = await client.post(
            url=os.getenv("TEST_URL_TRAFFIC"),  # type: ignore[]
            json=request_tpi_without_schemas,
            headers=headers,
        )
        assert result.status_code == 200
        assert result.json() == {
            "weather": response_api,
            "recommended_information": chat_gpt_response["message"],
            "traffic_jams_status": traffic_jams_good,
        }


async def test_collect_road_data_failure(client: AsyncClient):
    with mock.patch(
        "src.handlers.router.send_header_to_auth_service",
    ) as response_auth:
        response_auth.return_value = {
            "detail": "detail",
            "status_code": status.HTTP_401_UNAUTHORIZED,
        }
        result = await client.post(
            url=os.getenv("TEST_URL_TRAFFIC"),  # type: ignore[]
            json=request_tpi_without_schemas,
            headers=headers,
        )
        assert result.status_code == 401
        assert result.json() == {
            "message": "detail",
        }


async def test_collect_road_data_without_headers(client: AsyncClient):
    result = await client.post(
        url=os.getenv("TEST_URL_TRAFFIC"),  # type: ignore[]
        json=request_tpi_without_schemas,
    )
    assert result.status_code == 401
    assert (
        result.json()["message"] == "check Authorization token, and try again"
    )


async def test_collect_road_data_without_query_params(client: AsyncClient):
    result = await client.post(
        url=os.getenv("TEST_URL_TRAFFIC"),  # type: ignore[]
    )
    assert result.status_code == 422
