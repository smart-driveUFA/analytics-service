import os

from aiohttp import ClientSession
from fastapi import status


async def send_header_to_auth_service(headers: dict):
    url = os.getenv("AUTH_CHECK_TOKEN_URL")
    async with ClientSession() as session, session.post(
        url,
        headers=headers,
    ) as response:
        await session.close()
        if response.status == status.HTTP_200_OK:
            return {
                "message": "token is valid",
                "status": response.status,
            }
        elif response.status == status.HTTP_404_NOT_FOUND:
            return {
                "message": "token is invalid",
                "status": response.status,
            }
        else:
            return {
                "message": "something going wrong, try again or write to {email}",
                "status": response.status,
            }
