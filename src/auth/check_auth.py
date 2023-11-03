import os

import requests


async def send_header_to_auth_service(headers: dict) -> dict:
    """
    Send request to auth_service for authentication headers from request
    :param headers: Authorization Bearer
    :return: response message auth_service and status code
    """
    url = os.getenv("AUTH_CHECK_TOKEN_URL")
    response = requests.post(url, headers=headers, timeout=(1, 1))
    return {
        "message": response.json(),
        "status": response.status_code,
    }
