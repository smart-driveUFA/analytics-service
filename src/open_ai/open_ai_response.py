import os
from typing import Union

import requests
from fastapi import APIRouter
from starlette import status

from src.mongodb.mongo import client_mongo
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


async def response_openai(weather: dict) -> Union[str, None]:
    message = await _convert_data_to_message_openai(weather)
    if isinstance(message, str):
        return await _send_request_openai_chat_completion(message)
    return None
