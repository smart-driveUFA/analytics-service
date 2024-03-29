import json
import os
from typing import Union

import requests
from aioredis.connection import EncodableT
from fastapi import status

from src.database.mongo import client_mongo
from src.database.redis import redis_client
from src.utils import Url


async def _get_weather(lat: float, lon: float, count: int = 1) -> dict:
    """
    Make request to yandex weather API;
    :param lat: latitude of an object;
    :param lon: longitude of an object;
    :param count: quantity of days in request;
    :return: yandex weather or None'
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
    return {}


async def _convert_yandex_weather_to_dict(yandex: dict) -> dict:
    """
    Make a dict result for a client from yandex weather api;
    :param yandex: dict yandex weather api;
    :return: dict weather;
    """
    if isinstance(yandex, dict):
        geo_object: dict = yandex["geo_object"]["locality"]
        fact: dict = yandex["fact"]
        result: dict = {
            "city": geo_object["name"],
            "temperature": fact["temp"],
            "feels_like": fact["feels_like"],
            "condition": fact["condition"],
            "pressure_mm": fact["pressure_mm"],
            "pressure_pa": fact["pressure_pa"],
            "humidity": fact["humidity"],
            "wind_gust": fact["wind_gust"],
        }
        await client_mongo["response_weather"].insert_one(result)
        result.pop("_id", None)
        return result
    else:
        return {}


async def processed_data_weather(
    lat: float,
    lon: float,
) -> Union[dict, None]:
    """
    if not cache, call _get_weather and save it to redis;
    :param lat: latitude of location;
    :param lon: longitude of location;
    :return: dict _convert_yandex_weather_to_dict;
    """
    _name = f"yandex weather {lat}-{lon}"
    cached_data = await redis_client.get(name=_name)
    if cached_data:
        return await _convert_yandex_weather_to_dict(cached_data)
    weather = await _get_weather(lat, lon)
    if not isinstance(weather, EncodableT):
        if isinstance(weather, dict) and weather["_id"]:
            weather.pop("_id")
        convert_to_encodable = json.dumps(weather)
    else:
        convert_to_encodable = weather
    await redis_client.set(name=_name, value=convert_to_encodable)
    result = await _convert_yandex_weather_to_dict(weather)
    return result if result else None
