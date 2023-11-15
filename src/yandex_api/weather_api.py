import copy
import os
from typing import Union

from aiohttp import ClientSession
from fastapi import APIRouter, status

from src.database.mongo import client_mongo
from src.database.redis import redis_client
from src.utils import Url

router = APIRouter(
    prefix="/yandex_api",
    tags=["yandex_api"],
)


async def _get_weather(lat: float, lon: float, count: int = 1) -> Union[dict, None]:
    """
    Make request to yandex.weather API
    :param lat: latitude of object
    :param lon: longitude of object
    :param count: quantity of days in request
    :return: yandex weather or None
    """
    url = Url(lat, lon, count).weather
    headers = {
        "X-Yandex-API-Key": str(os.getenv("WEATHER_YANDEX")),
    }
    async with ClientSession() as session:
        response = await session.get(url, headers=headers)
        response_json = await response.json()
        await session.close()
    if (
        response.status == status.HTTP_200_OK
        and response_json["geo_object"]
        and response_json["fact"]
    ):
        value_for_mongodb = copy.deepcopy(response_json)
        await client_mongo["yandex"].insert_one(value_for_mongodb)
        return response_json
    return None


async def _convert_yandex_weather_to_dict(yandex: dict) -> dict:
    """
    Make ResponseAPI data from yandex.weather api
    :param yandex: dict yandex.weather api
    :return: dict ResponseAPI
    """
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
    value_for_mongodb = copy.deepcopy(result)
    await client_mongo["response_weather"].insert_one(value_for_mongodb)
    return result


async def processed_data_weather(
    lat: float, lon: float, count: int = 1
) -> Union[dict, None]:
    _name = f"yandex weather{lat}-{lon}"
    _time_to_store = 120
    cached_data = await redis_client.get(name=_name)
    if cached_data:
        return await _convert_yandex_weather_to_dict(cached_data)
    weather = await _get_weather(lat, lon, count)
    if weather:
        await redis_client.set(name=_name, value=weather, lifetime=_time_to_store)
        return await _convert_yandex_weather_to_dict(weather)
    else:
        return None
