import os

import requests


async def send_header_to_auth_service(token: str) -> bool:
    """
    Send request to auth_service for authentication headers from request
    :param token: Authorization Bearer
    :return: token verification status
    """
    headers = {
        "Authorization": token,
    }
    url = os.getenv("AUTH_CHECK_TOKEN_URL")
    response = requests.post(url, headers=headers, timeout=(1, 1))
    return response.status_code == 200
