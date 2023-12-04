import os

import requests

from src.handlers.schemas import TPI


async def request_auth_create_tpi(
    tpi_data: TPI,
    token: str,
    end_lat: float,
    end_lon: float,
) -> bool:
    """
    Send request to auth_service for authentication headers from request and request for create tpi
    :param end_lon:
    :param end_lat:
    :param tpi_data:
    :param token: Authorization Bearer
    :return: create verification status
    """
    headers = {
        "Authorization": token,
    }
    url = os.getenv("AUTH_TPI_URL")
    try:
        data = tpi_data.model_dump()
        data["lat_end"] = end_lat
        data["lon_end"] = end_lon
        response = requests.post(url, data=data, headers=headers, timeout=(1, 1))
        return response.status_code == 201
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False
