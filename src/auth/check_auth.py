import os

import requests


async def send_header_to_auth_service(token: str, lat: float, lon: float) -> bool:
    """
    Send request to auth_service for authentication headers from request
    :param lat: coordinate parameters latitude location
    :param lon: coordinate parameters latitude location
    :param token: Authorization Bearer
    :return: token verification status
    """
    headers = {
        "Authorization": token,
    }
    coordinates = {
        "lat": lat,
        "lon": lon,
    }
    url = os.getenv("AUTH_CHECK_TOKEN_URL")
    response = requests.post(url, headers=headers, json=coordinates, timeout=(1, 1))
    return response.status_code == 200
