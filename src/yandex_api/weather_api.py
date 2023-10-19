import os

import requests
from fastapi import APIRouter, status

from src.mongodb.mongo import client_mongo
from src.yandex_api.schemas import ResponseMongodbObjectId
from src.yandex_api.utils import Url

router = APIRouter(
    prefix="/yandex_api",
    tags=["yandex_api"],
)


@router.post(
    "/weather",
    response_model=ResponseMongodbObjectId,
    status_code=status.HTTP_201_CREATED,
)
async def get_weather(lat: float, lon: float, count: int = 1):
    url = Url(lat, lon, count)
    headers = {"X-Yandex-API-Key": os.getenv("WEATHER_YANDEX")}
    response_json = requests.get(url.url, headers=headers, timeout=(1, 2)).json()
    return await client_mongo.insert_one("yandex", response_json)
