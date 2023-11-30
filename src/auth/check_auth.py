import os

import requests


async def send_header_to_auth_service(token: str) -> bool:
    """
    Send request to auth_service for authentication headers from request
    :param token: Authorization Bearer
    :return: token verification status True or False
    """
    headers = {
        "Authorization": token,
    }
    url = os.getenv("AUTH_CHECK_TOKEN_URL")
    try:
        response = requests.get(url, headers=headers, timeout=(1, 1))
        return response.status_code == 200
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False
