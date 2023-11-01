import os

from aiohttp import ClientSession
from fastapi import status


async def request_auth_create_tpi(
    lat: float,
    lon: float,
    direction: str,
    headers: dict,
):
    """
    Send request to auth_service for authentication headers from request and request for create tpi
    :param lat: tpi's latitude
    :param lon: tpi's longitude
    :param direction: direction of movement
    :param headers: Authorization Bearer
    :return: response message auth_service and status code
    """
    data = {
        "latitude": lat,
        "longitude": lon,
        "direction": direction,
    }
    url = os.getenv("AUTH_CREATE_TPI_URL")
    async with ClientSession() as session, session.post(
        url,
        data=data,
        headers=headers,
    ) as response:
        await session.close()
    match response.status:
        case status.HTTP_201_CREATED:
            return {
                "message": "TPI was created successfully",
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
