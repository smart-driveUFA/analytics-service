from typing import Dict, Union

import requests
from starlette import status

from src.database.mongo import client_mongo
from src.database.redis import redis_client
from src.utils import Url


async def _send_request_2gis(
    lat_start: float, lon_start: float, lat_end: float, lon_end: float
):
    """
    send request to 2gis and
    :return: response 2gis part of a result
    """
    url = Url().to_gis
    data = {
        "points": [
            {
                "type": "stop",
                "lon": lat_start,
                "lat": lon_start,
            },
            {
                "type": "stop",
                "lon": lat_end,
                "lat": lon_end,
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


async def _count_time_route(params_router: Dict[str, int]) -> Union[int, None]:
    """
    count travels time using length and duration
    :param params_router: dict with key duration and length
    :return: str status of traffic jams
    """
    seconds_to_hours = 3600
    meters_to_kilos = 1000
    length_of_road = 35
    grade_of_jams_city = {
        0: range(80, 90),
        1: range(70, 80),
        2: range(60, 70),
        3: range(50, 60),
        4: range(40, 50),
        5: range(30, 40),
        6: range(25, 30),
        7: range(20, 25),
        8: range(15, 20),
        9: range(10, 15),
        10: range(10),
    }
    grade_of_jams_highway = {
        0: range(130, 150),
        1: range(110, 130),
        2: range(90, 110),
        3: range(70, 90),
        4: range(50, 70),
        5: range(40, 50),
        6: range(30, 40),
        7: range(20, 30),
        8: range(15, 20),
        9: range(10, 15),
        10: range(10),
    }
    if isinstance(params_router["duration"], (int, float)) and isinstance(
        params_router["length"], (int, float)
    ):
        km = params_router["length"] / meters_to_kilos  # 51.709
        time = params_router["duration"] / seconds_to_hours  # 1.01
        average_speed = km / time  # 50.246
        if km >= length_of_road:
            type_of_grade = grade_of_jams_highway
        else:
            type_of_grade = grade_of_jams_city
        for k, v in type_of_grade.items():
            if int(average_speed) in v:
                return k
        return None
    else:
        return None


async def status_road_speed(
    lat_start: float, lon_start: float, lat_end: float, lon_end: float
):
    """
    if not cache call _send_request_2gis and _count_time_route and save response to redis
    :param lon_end:
    :param lat_end:
    :param lon_start:
    :param lat_start:
    :return: dict params about a road with keys duration length status of traffic jams
    """
    _key_of_cache = f"{lat_start, lon_start}" f"-{lat_end, lon_end}"
    cached_data = await redis_client.get(name=_key_of_cache)
    if cached_data:
        return cached_data
    time_and_length = await _send_request_2gis(lat_start, lon_start, lat_end, lon_end)
    if time_and_length:
        status_of_jams = await _count_time_route(time_and_length)
        if isinstance(status_of_jams, (int, float)):
            time_and_length["status_of_jams"] = status_of_jams
        await redis_client.set(name=_key_of_cache, value=time_and_length)
        return time_and_length
    else:
        return None
