from typing import Dict

import requests
from fastapi import APIRouter
from starlette import status

from src.database.mongo import client_mongo
from src.database.redis import redis_client
from src.handlers.schemas import CoordinatesBetweenTPI
from src.utils import Url

router = APIRouter(
    prefix="/check",
    tags=["router_api"],
)


@router.post(
    "/2gis",
)
async def _send_request_2gis(coordinate_of_route: CoordinatesBetweenTPI):
    """
    send request to 2gis and
    :param coordinate_of_route: coordinate parameters start and stop location
    :return: response 2gis part of result
    """
    url = Url().to_gis
    data = {
        "points": [
            {
                "type": "stop",
                "lon": coordinate_of_route.start.lon,
                "lat": coordinate_of_route.start.lat,
            },
            {
                "type": "stop",
                "lon": coordinate_of_route.stop.lon,
                "lat": coordinate_of_route.stop.lat,
            },
        ],
        "locale": "ru",
        "transport": "car",
        "route_mode": "fastest",
        "traffic_mode": "jam",
        "output": "summary",
    }

    response = requests.post(url=url, json=data, timeout=(1, 2))

    match response.status_code:
        case status.HTTP_200_OK:
            if response.json()["status"] == "OK":
                client_mongo["response_2gis"].insert_one(response.json())
                return response.json()["result"][0]
            return None
        case _:
            return None


async def _count_time_route(params_router: Dict[str, int]):
    """
    count travels time using length and duration
    :param params_router: dict with key duration and length
    :return: str status of traffic jams
    """
    minutes_to_hours = 60
    meters_to_kilos = 1000
    normal_time = 1.3
    if isinstance(params_router["duration"], (int, float)) and isinstance(
        params_router["length"], (int, float)
    ):
        duration = params_router["length"] / meters_to_kilos
        time_in_minute = params_router["duration"] / minutes_to_hours
        average_speed = duration / time_in_minute
        #  что нужно выводить ВОПРОС
        if average_speed >= normal_time:
            return "normal"
        elif average_speed < normal_time:
            return "high"
        else:
            return None
    else:
        raise TypeError("expected int or float")


async def status_road_speed(coordinate_of_route: CoordinatesBetweenTPI):
    """
    if not cache call _send_request_2gis and _count_time_route and save response to redis
    :param coordinate_of_route: coordinate parameters start and stop location
    :return: dict params about road with keys duration length status of traffic jams
    """
    _key_of_cache = (
        f"{coordinate_of_route.start.lat, coordinate_of_route.start.lon}"
        f"-{coordinate_of_route.stop.lat, coordinate_of_route.stop.lon}"
    )
    cached_data = await redis_client.get(name=_key_of_cache)
    if cached_data:
        return cached_data
    time_and_length = await _send_request_2gis(coordinate_of_route)
    if time_and_length:
        time_and_length["status_of_jams"] = await _count_time_route(time_and_length)
        await redis_client.set(name=_key_of_cache, value=time_and_length)
        return time_and_length
    else:
        return None
