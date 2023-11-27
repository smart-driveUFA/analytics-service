from unittest.mock import patch

from dirty_equals import IsFloat, IsInt, IsStr
from starlette import status

from src.yandex_api.weather_api import _convert_yandex_weather_to_dict, _get_weather
from tests.fixture import response_yandex_example, start_data


async def test_convert_yandex_to_dict_right():
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


@patch("src.yandex_api.weather_api.requests")
async def test__get_weather_forbidden(mock_requests_403):
    mock_requests_403.get.return_value.status_code = status.HTTP_403_FORBIDDEN
    result = await _get_weather(start_data["lat"], start_data["lon"])
    assert result is None
