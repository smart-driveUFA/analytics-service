import os

from aiohttp import ClientSession
from fastapi import APIRouter, status

from src.mongodb.mongo import client_mongo
from src.yandex_api.schemas import ResponseAPI
from src.yandex_api.utils import Url

router = APIRouter(
    prefix="/yandex_api",
    tags=["yandex_api"],
)


@router.get(
    "/get-weather",
    response_model=ResponseAPI,
    status_code=status.HTTP_201_CREATED,
)
async def get_weather(lat: float, lon: float, count: int = 1) -> ResponseAPI | dict:
    """
    Make request to yandex.weather API
    :param lat: latitude of object
    :param lon: longitude of object
    :param count: quantity of days in request
    :return: dict ResponseAPI or error message
    """
    url = Url(lat, lon, count).weather
    headers = {
        "X-Yandex-API-Key": str(os.getenv("WEATHER_YANDEX")),
        "content-type": "application/json",
    }
    async with ClientSession() as session:
        response = await session.get(url, headers=headers)
        response_json = await response.json()
        await session.close()
        if response.status == status.HTTP_200_OK:
            if response_json["geo_object"] and response_json["fact"]:
                await client_mongo["yandex"].insert_one(response_json)
                return await convert_yandex_to_dict(response_json)
            else:
                return {
                    "message": "response returned wrong data, please check request",
                    "response": response_json,
                }
        elif response.status == status.HTTP_404_NOT_FOUND:
            return {
                "message": "The data entered is incorrect, please check the data and try again.",
                "status": response.status,
            }
        elif response.status == status.HTTP_403_FORBIDDEN:
            return {"message": "request not allows", "status": response.status}
        else:
            return {
                "message": "Something going wrong",
                "status": response.status,
            }


async def convert_yandex_to_dict(yandex: dict) -> ResponseAPI:
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
    await client_mongo["responses"].insert_one(result)
    return ResponseAPI.model_validate(result)
