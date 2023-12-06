import os
from typing import Union

import requests
from starlette import status

from src.database.mongo import client_mongo
from src.database.redis import redis_client
from src.utils import Url


async def _send_request_openai_chat_completion(message: str) -> Union[dict, None]:
    """
    sends a request to the gpt chat and returns the analyzed data;
    :param message: chat message gpt in the content field;
    :return: response chatgpt field content;
    """
    url = Url().open_ai
    open_api_key = os.getenv("OPEN_AI_KEY")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {open_api_key}",
    }
    data = {
        "model": os.getenv("MODEL_OPENAI"),
        "messages": [{"role": "user", "content": message}],
        "temperature": 0.1,
    }
    response = requests.post(url=url, headers=headers, json=data)  # noqa: S113
    match response.status_code:
        case status.HTTP_200_OK:
            await client_mongo["response_chatgpt"].insert_one(response.json())
            return (
                response.json()["choices"][0]["message"]["content"] or response.json()
            )
        case _:
            return None


async def _convert_data_to_message_openai(weather: dict) -> str:
    """
    Create a task to chatgpt;
    :param weather: weather of a road with coordinates;
    :return: message from chatgpt;
    """
    task = (
        "Исходя из приведенных данных проведи анализ погодных условий и "
        "сделай вывод о возможности гололеда и других погодных ситуаций"
    )
    information_of_road = ""
    if isinstance(weather, dict):
        for key, value in weather.items():
            information_of_road += f"{key}: {value} "
    return f"{task} {information_of_road}" if information_of_road else None


async def response_openai(weather: dict, lat: float, lon: float) -> Union[dict, None]:
    """
    if not cache create a message to chatgpt and call _send_request_openai_chat_completion
    and save response to redis;
    :param weather: takes current weather in location;
    :param lat: latitude of location;
    :param lon: longitude of location;
    :return:
    """
    name_cached_data = f"openai response {lat}-{lon}."
    cached_data = await redis_client.get(name=name_cached_data)
    if cached_data:
        return cached_data
    message = await _convert_data_to_message_openai(weather)
    if message:
        response_chatgpt = await _send_request_openai_chat_completion(message)
        if response_chatgpt:
            await redis_client.set(name=name_cached_data, value=response_chatgpt)
            return response_chatgpt
    return None
