import ast
import os
from typing import Union

import requests
from starlette import status

from src.database.mongo import client_mongo
from src.database.redis import redis_client
from src.utils import Url


async def _get_weather(lat: float, lon: float, count: int = 1) -> dict | None:
    """
    Make request to yandex weather API;
    :param lat: latitude of an object;
    :param lon: longitude of an object;
    :param count: quantity of days in request;
    :return: yandex weather or None
    """
    url = Url(lat, lon, count).weather
    headers = {
        "X-Yandex-API-Key": str(os.getenv("WEATHER_YANDEX")),
    }
    try:
        response = requests.get(url=url, headers=headers)  # noqa: S113
    except requests.Timeout:
        return {}
    except requests.ConnectionError:
        return {}
    if response.status_code == status.HTTP_200_OK:
        response_json = response.json()
        await client_mongo["yandex"].insert_one(response_json)
        response_json.pop("_id", None)
        return response_json
    return None


async def _convert_yandex_weather_to_dict(yandex: dict, cache_key: str) -> dict | None:
    """
    Make a dict result for a client from yandex weather api;
    :param yandex: dict yandex weather api;
    :return: dict weather;
    """
    cached_data = await redis_client.get(name=cache_key)
    if cached_data:
        return ast.literal_eval(cached_data)
    if isinstance(yandex, dict):
        geo_object = yandex["geo_object"]["locality"]
        fact = yandex["fact"]
        result = {
            "city": geo_object["name"],
            "temperature": fact["temp"],
            "feels_like": fact["feels_like"],
            "condition": fact["condition"],
            "pressure_mm": fact["pressure_mm"],
            "pressure_pa": fact["pressure_pa"],
            "humidity": fact["humidity"],
            "wind_gust": fact["wind_gust"],
        }
        await redis_client.set(name=cache_key, value=str(result))
        await client_mongo["response_weather"].insert_one(result)
        if "_id" in result:
            result.pop("_id", None)
        return result
    return None


async def processed_data_weather(
    lat: float,
    lon: float,
) -> Union[dict, None]:
    """
    if not cache, call _get_weather and convert it to response dict;
    :param lat: latitude of location;
    :param lon: longitude of location;
    :return: response dict or None
    """
    cache_key = f"yandex weather {lat}-{lon}"
    cached_data = await redis_client.get(name=cache_key)
    if cached_data:
        return ast.literal_eval(cached_data)
    weather = await _get_weather(lat, lon)
    if weather is not None:
        if "_id" in weather:
            weather.pop("_id")
        result = await _convert_yandex_weather_to_dict(weather, cache_key)
        return result if result else None
    return None
