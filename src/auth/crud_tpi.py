import os

from aiohttp import ClientSession
from fastapi import status


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
    async with ClientSession() as session, session.post(
        url,
        data=data,
        headers=headers,
    ) as response:
        await session.close()
    if response.status == status.HTTP_201_CREATED:
        return {
            "message": "TPI was created successfully",
            "status": response.status,
        }
    else:
        return {
            "message": "something going wrong, try again or write to {email}",
            "status": response.status,
        }
