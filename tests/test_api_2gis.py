from unittest import mock

from requests import Timeout
from starlette import status

from src.api_2gis.too_gis import status_road_speed
from tests.fixture import (
    for_2gis_req,
    response_2gis_api,
    response_2gis_api_bad_status,
    traffic_jams,
    traffic_jams_good,
)


@mock.patch("src.api_2gis.too_gis.requests")
async def test__send_request_2gis(mock_requests):
    mock_requests.post.return_value.status_code = status.HTTP_200_OK
    mock_requests.post.return_value.json = mock.Mock(return_value=response_2gis_api)
    from src.api_2gis.too_gis import _send_request_2gis

    response = await _send_request_2gis(
        for_2gis_req["lat_start"],
        for_2gis_req["lon_start"],
        for_2gis_req["lat_end"],
        for_2gis_req["lon_end"],
    )
    assert response == traffic_jams_good


@mock.patch("src.api_2gis.too_gis.requests")
async def test__send_request_2gis_bad_status(mock_requests):
    mock_requests.post.return_value.status_code = status.HTTP_400_BAD_REQUEST
    from src.api_2gis.too_gis import _send_request_2gis

    response = await _send_request_2gis(
        for_2gis_req["lat_start"],
        for_2gis_req["lon_start"],
        for_2gis_req["lat_end"],
        for_2gis_req["lon_end"],
    )
    assert response is None


@mock.patch("src.api_2gis.too_gis.requests")
async def test__send_request_2gis_bad_response(mock_requests):
    mock_requests.post.return_value.status_code = status.HTTP_200_OK
    mock_requests.post.return_value.json = mock.Mock(
        return_value=response_2gis_api_bad_status
    )
    from src.api_2gis.too_gis import _send_request_2gis

    response = await _send_request_2gis(
        for_2gis_req["lat_start"],
        for_2gis_req["lon_start"],
        for_2gis_req["lat_end"],
        for_2gis_req["lon_end"],
    )
    assert response is None


async def test__send_request_2gis_timeout_error():
    with mock.patch("src.api_2gis.too_gis.requests.post", side_effect=Timeout):
        from src.api_2gis.too_gis import _send_request_2gis

        result = await _send_request_2gis(
            for_2gis_req["lat_start"],
            for_2gis_req["lon_start"],
            for_2gis_req["lat_end"],
            for_2gis_req["lon_end"],
        )
        assert result is None


async def test__send_request_2gis_connection_error():
    with mock.patch("requests.post", side_effect=ConnectionError):
        from src.api_2gis.too_gis import _send_request_2gis

        result = await _send_request_2gis(
            for_2gis_req["lat_start"],
            for_2gis_req["lon_start"],
            for_2gis_req["lat_end"],
            for_2gis_req["lon_end"],
        )
        assert result is None


async def test__count_time_route():
    from src.api_2gis.too_gis import _count_time_route

    response = await _count_time_route(traffic_jams_good)
    assert response == 10


async def test__count_time_route_bad_type():
    from src.api_2gis.too_gis import _count_time_route

    response = await _count_time_route(
        {
            "duration": "",  # type: ignore[only for test]
            "length": 123,
        }
    )
    assert response is None


async def test__count_time_route_too_many_speed():
    from src.api_2gis.too_gis import _count_time_route

    response = await _count_time_route(
        {
            "duration": 1,
            "length": 1230,
        }
    )
    assert response is None


async def test__count_time_route_too_many_distance():
    from src.api_2gis.too_gis import _count_time_route

    response = await _count_time_route(
        {
            "duration": 10000,
            "length": 1230123312,
        }
    )
    assert response is None


async def test_status_road_speed():
    with mock.patch(
        "src.api_2gis.too_gis._send_request_2gis",
        return_value=traffic_jams,
    ), mock.patch(
        "src.api_2gis.too_gis._count_time_route",
        return_value=4,
    ):
        response = await status_road_speed(
            for_2gis_req["lat_start"],
            for_2gis_req["lon_start"],
            for_2gis_req["lat_end"],
            for_2gis_req["lon_end"],
        )
        assert response == traffic_jams_good
