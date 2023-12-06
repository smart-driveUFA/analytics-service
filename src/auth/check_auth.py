import os

import requests

from src.handlers.schemas import TPI


async def send_header_to_auth_service(token: str, route_coor: TPI):
    """
    Send request to auth_service for authentication headers from request
    :param route_coor:
    :param token: Authorization Bearer
    :return: token verification status True or False
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
    except requests.ConnectionError:
        return None, None
    except requests.Timeout:
        return None, None
    if response.status_code == 200:
        return {
            "lat_end": response.json()["lat_end"],
            "lon_end": response.json()["lon_end"],
        }
    return {"detail": response.json()["detail"], "status_code": response.status_code}
