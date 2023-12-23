from unittest.mock import AsyncMock, Mock, patch

from dirty_equals import IsFloat, IsInt, IsStr
from requests.exceptions import ConnectionError, Timeout
from starlette import status

from src.yandex_api.weather_api import processed_data_weather
from tests.fixture import response_api, response_yandex_example, start_data


async def test_convert_yandex_to_dict_right():
    from src.yandex_api.weather_api import _convert_yandex_weather_to_dict

    result = await _convert_yandex_weather_to_dict(response_yandex_example)
    assert result["city"] == "Москва"
    assert result["city"] == IsStr
    assert result["temperature"] == IsInt
    assert result["feels_like"] == IsInt
    assert result["condition"] == IsStr
    assert result["pressure_mm"] == IsInt
    assert result["pressure_pa"] == IsInt
    assert result["humidity"] == IsInt
    assert result["wind_gust"] == IsFloat


async def test_processed_data_weather_without_weather():
    mock_get_weather = AsyncMock(
        return_value=None,
    )
    with patch("src.yandex_api.weather_api._get_weather", mock_get_weather):
        result = await processed_data_weather(start_data["lat"], start_data["lon"])
        assert result is None


@patch("src.yandex_api.weather_api.requests")
async def test__get_weather_forbidden(mock_requests_403):
    mock_requests_403.get.return_value.status_code = status.HTTP_403_FORBIDDEN
    from src.yandex_api.weather_api import _get_weather

    result = await _get_weather(start_data["lat"], start_data["lon"])
    assert result is None


async def test__get_weather_timeout_error():
    with patch("src.api_2gis.too_gis.requests.get", side_effect=Timeout):
        from src.yandex_api.weather_api import _get_weather

        result = await _get_weather(start_data["lat"], start_data["lon"])
        assert result is None


async def test__get_weather_connection_error():
    with patch(
        "src.api_2gis.too_gis.requests.get",
        side_effect=ConnectionError,
    ):
        from src.yandex_api.weather_api import _get_weather

        result = await _get_weather(start_data["lat"], start_data["lon"])
        assert result is None


@patch("src.yandex_api.weather_api.requests")
async def test__get_weather(mock_requests):
    mock_requests.get.return_value.status_code = status.HTTP_200_OK
    mock_requests.get.return_value.json = Mock(return_value=response_yandex_example)
    from src.yandex_api.weather_api import _get_weather

    result = await _get_weather(start_data["lat"], start_data["lon"])
    assert result == response_yandex_example


async def test_processed_data_weather():
    mock_get_weather = AsyncMock(
        return_value=response_yandex_example,
    )
    with patch("src.yandex_api.weather_api._get_weather", mock_get_weather):
        result = await processed_data_weather(start_data["lat"], start_data["lon"])
        assert result == response_api


async def test_processed_data_weather_with_cache():
    mock_cache = AsyncMock(
        return_value=response_yandex_example,
    )
    with patch("src.yandex_api.weather_api.redis_client.get", mock_cache):
        result = await processed_data_weather(start_data["lat"], start_data["lon"])
        assert result == response_api
