import os

from aiohttp import ClientSession


async def send_result_auth(
    processed_data: dict, token: str, lat: float, lon: float
) -> None:
    """
    make async request to sending result response of service;
    :param processed_data: return data for clients;
    :param token: user's bearer token;
    :param lat: tpi's latitude;
    :param lon: tpi's longitude;
    :return: None
    """
    headers = {
        "Authorization": token,
    }
    processed_data["lat"] = lat
    processed_data["lon"] = lon
    async with ClientSession() as session, session.post(
        os.getenv("AUTH_CHECK_REQUEST_COUNT"), data=processed_data, headers=headers
    ) as resp:
        resp.close()
