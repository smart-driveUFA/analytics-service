import os

import requests

from src.handlers.schemas import CreateTPI


async def request_auth_create_tpi(
    tpi_data: CreateTPI,
    token: str,
) -> bool:
    """
    Send request to auth_service for authentication headers from request and request for create tpi
    :param tpi_data:
    :param token: Authorization Bearer
    :return: create verification status
    """
    headers = {
        "Authorization": token,
    }
    url = os.getenv("AUTH_CREATE_TPI_URL")
    try:
        response = requests.post(
            url, data=tpi_data.model_dump(), headers=headers, timeout=(1, 1)
        )
        return response.status_code == 201
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False
