import os

from aiohttp import ClientSession


async def request_auth_create_tpi(
    lat: float,
    lon: float,
    direction: str,
    headers: dict,
):
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
