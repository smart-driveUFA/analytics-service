import os

import requests
from fastapi import APIRouter

from src.mongodb.mongo import client_mongo
from src.yandex_api.schemas import ResponseAPI
from src.yandex_api.utils import Url

router = APIRouter(
    prefix="/yandex_api",
    tags=["yandex_api"],
)


async def get_weather(lat: float, lon: float, count: int = 1) -> ResponseAPI:
    """
    Make request to yandex.weather API
    :param lat: latitude of object
    :param lon: longitude of object
    :param count: quantity of days for request
    :return: dict ResponseAPI
    """
    url = Url(lat, lon, count)
    headers = {"X-Yandex-API-Key": os.getenv("WEATHER_YANDEX")}
    response_json = requests.get(url.weather, headers=headers, timeout=(1, 2)).json()
    await client_mongo.insert_one("yandex", response_json)
    result = await convert_yandex_to_dict(response_json)
    return result


async def convert_yandex_to_dict(yandex: dict) -> ResponseAPI:
    """
    Make ResponseAPI data from yandex.weather api
    :param yandex: dict yandex.weather api
    :return: dict ResponseAPI
    """
    geo_object: dict = yandex['geo_object']
    fact: dict = yandex['fact']
    result: dict = {
        "city": geo_object['locality']["name"],
        "temperature": fact["temp"],
        "feels_like": fact["feels_like"],
        "condition": fact["condition"],
        "pressure_mm": fact["pressure_mm"],
        "pressure_pa": fact["pressure_pa"],
        "humidity": fact["humidity"],
        "wind_gust": fact["wind_gust"],
    }
    await client_mongo.insert_one("responses", result)
    return ResponseAPI.model_validate(result)
