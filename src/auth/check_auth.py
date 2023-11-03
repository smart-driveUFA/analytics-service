import os

from aiohttp import ClientSession
from fastapi import status


async def send_header_to_auth_service(headers: dict) -> dict:
    """
    Send request to auth_service for authentication headers from request
    :param headers: Authorization Bearer
    :return: response message auth_service and status code
    """
    url = os.getenv("AUTH_CHECK_TOKEN_URL")
    async with ClientSession() as session, session.post(
        url,
        headers=headers,
    ) as response:
        await session.close()
    match response.status:
        case status.HTTP_200_OK:
            return {
                "message": "token is valid",
                "status": response.status,
            }
        case status.HTTP_404_NOT_FOUND:
            return {
                "message": "token not found",
                "status": response.status,
            }
        case status.HTTP_403_FORBIDDEN:
            return {
                "message": "token is invalid",
                "status": response.status,
            }
        case _:
            return {
                "message": "something going wrong, try again or write to {email}",
                "status": response.status,
            }
