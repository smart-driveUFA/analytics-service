import os
from typing import Any

import requests
from requests import Timeout

from src.handlers.schemas import TPI


async def send_header_to_auth_service(token: str, route_coor: TPI) -> dict[str, Any]:
    """
    make request for check token and take coordinates of end point route;
    :param route_coor: schema of tpi's params;
    :param token: Authorization Bearer;
    :return: lat and lon of end point route;
    """
    headers = {
        "Authorization": token,
    }
    url = os.getenv("AUTH_GET_COOR")
    data = {
        "lat_start": route_coor.lat_start,
        "lon_start": route_coor.lon_start,
        "start": route_coor.start,
        "end": route_coor.end,
        "highway": route_coor.highway,
    }
    try:
        response = requests.get(url, headers=headers, data=data, timeout=(1, 1))
    except ConnectionError:
        return {
            "lat_end": None,
            "lon_end": None,
        }
    except Timeout:
        return {
            "lat_end": None,
            "lon_end": None,
        }
    if response.status_code == 200:
        return {
            "lat_end": response.json()["lat_end"],
            "lon_end": response.json()["lon_end"],
        }
    return {"detail": response.json()["detail"], "status_code": response.status_code}
