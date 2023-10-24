import os

import requests
from fastapi import APIRouter, status

from src.mongodb.mongo import client_mongo
from src.yandex_api.schemas import ResponseMongodbObjectId
from src.yandex_api.utils import Url

router = APIRouter(
    prefix="/yandex_api",
    tags=["yandex_api"],
)


@router.post(
    "/yandexgpt",
    response_model=ResponseMongodbObjectId,
    status_code=status.HTTP_201_CREATED,
)
async def send_data_to_yandex_gpt(instruction_text: str, request_text: str):
    """
    Make request to yandexGPT api
    :return: id added object
    """
    headers = {
        "Bearer": os.getenv("IAM_YANDEX_TOKEN"),
        "x-folder-id": "b1g3rip01cqdmovr0l71",
        "Content-Type": "application/json",
    }
    data = {
        "model": "general",
        "generationOptions": {
            "partialResults": True,
            "temperature": 0.1,
            "maxTokens": 1500,
        },
        "instructionText": instruction_text,
        "requestText": request_text,
    }
    response_json = requests.post(Url().gpt, data=data, headers=headers, timeout=(1, 2)).json()
    return await client_mongo.insert_one("yandex_GPT", response_json)
