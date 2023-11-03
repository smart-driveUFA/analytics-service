import os

from aiohttp import ClientSession


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
    async with ClientSession() as session:
        response = await session.post(url, data=data, headers=headers)
        await session.close()
    return {
        "message": await response.json(),
        "status": response.status,
    }
