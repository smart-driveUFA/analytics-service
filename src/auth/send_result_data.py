import os

from aiohttp import ClientSession
from src.handlers.schemas import TPI


async def send_result_auth(
    processed_data: dict, token: str, route_coor: TPI
) -> None:
    """
    make async request to sending result response of service;
    :param route_coor:
    :param processed_data: return data for clients;
    :param token: user's bearer token;
    :return: None
    """
    headers = {
        "Authorization": token,
    }
    tpi = {
        "lat_start": route_coor.lat_start,
        "lon_start": route_coor.lon_start,
        "start": route_coor.start,
        "end": route_coor.end,
        "highway": route_coor.highway
    }
    url = os.getenv("AUTH_CHECK_REQUEST_COUNT")
    processed_data["tpi"] = tpi
    for data_key in ["recommended_information", "weather", "traffic_jams_status"]:
        if isinstance(processed_data[data_key], dict) and "_id" in processed_data[data_key]:
            del processed_data[data_key]["_id"]

    if isinstance(url, str):
        async with ClientSession() as session, session.post(
                url,
                json=processed_data,
                headers=headers,
        ) as resp:
            resp.close()
