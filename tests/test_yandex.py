from dirty_equals import IsFloat, IsInt, IsStr

from src.yandex_api.weather_api import _convert_yandex_weather_to_dict
from tests.fixture import response_yandex_example


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
