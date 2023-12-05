import os
from typing import Union

import requests

from src.handlers.schemas import TPI


async def request_auth_create_tpi(
    tpi_data: TPI,
    token: str,
    end_lat: float,
    end_lon: float,
) -> Union[bool, dict]:
    """
    making request for creation tpi;
    :param end_lon: longitude of end point;
    :param end_lat: latitude of end point;
    :param tpi_data: schema of tpi's params;
    :param token: Authorization Bearer;
    :return: create verification status;
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
        if response.status_code == 400:
            return response.json()
        return response.status_code == 200
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False
