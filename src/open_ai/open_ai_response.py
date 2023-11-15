import os
from typing import Union

import requests
from fastapi import APIRouter
from starlette import status

from src.database.mongo import client_mongo
from src.database.redis import redis_client
from src.utils import Url

router = APIRouter(
    prefix="/routers",
    tags=["router_api"],
)


async def _send_request_openai_chat_completion(message: str) -> Union[dict, None]:
    """
    sends a request to the gpt chat and returns the analyzed data
    :param message: chat message gpt in the content field
    :return: response chatgpt field content
    """
    url = Url().open_ai
    open_api_key = os.getenv("OPEN_AI_KEY")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {open_api_key}",
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": message}],
        "temperature": 0.1,
    }
    response = requests.post(url=url, headers=headers, json=data)  # noqa: S113
    match response.status_code:
        case status.HTTP_200_OK:
            await client_mongo["response_chatgpt"].insert_one(response.json())
            return {
                "message": response.json()["choices"][0]["message"]["content"],
            }
        case _:
            return None


async def _convert_data_to_message_openai(weather: dict) -> str:
    """
    Create task for message to chatgpt
    :param weather: information about road with coordinates
    :return: message to chatgpt
    """
    task = (
        "Исходя из приведенных данных проведи анализ погодных условий и "
        "сделай вывод о возможности гололеда и других погодных ситуаций"
    )
    information_of_road = ""
    for key, value in weather.items():
        information_of_road += f"{key}: {value} "
    return f"{task} {information_of_road}"


async def response_openai(weather: dict, lat: float, lon: float) -> Union[dict, None]:
    message = await _convert_data_to_message_openai(weather)
    name_cached_data = f"openai response {lat}-{lon}."
    cached_data = await redis_client.get(name=name_cached_data)
    if cached_data:
        return cached_data
    response_chatgpt = await _send_request_openai_chat_completion(message)
    if response_chatgpt:
        await redis_client.set(name=name_cached_data, value=response_chatgpt["message"])
        return response_chatgpt
    return None
