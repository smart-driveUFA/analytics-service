from typing import Union

from fastapi import APIRouter, status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.auth.check_auth import send_header_to_auth_service
from src.auth.crud_tpi import request_auth_create_tpi
from src.handlers.schemas import CreateTPI
from src.open_ai.open_ai_response import response_openai
from src.yandex_api.schemas import ResponseAPI
from src.yandex_api.weather_api import processed_data_weather

router = APIRouter(
    prefix="/routers",
    tags=["router_api"],
)


@router.post(
    "/create-tpi",
    response_model=ResponseAPI | dict,
)
async def create_tpi(request: Request, tpi_data: CreateTPI):
    """
    Accepts the request to create tpi with params
    :param request: info about request
    :param tpi_data: schema of data
    :return: generated weather dictionary from location data
    """
    if request.headers.get("Authorization", None):
        tpi_response = await request_auth_create_tpi(
            tpi_data.lat,
            tpi_data.lon,
            tpi_data.direction,
            request.headers["Authorization"],
        )
        return JSONResponse(
            status_code=tpi_response["status"],
            content=tpi_response["message"],
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "message": "provide an access token",
            },
        )


@router.get(
    "/traffic-status",
    response_model=Union[str, ResponseAPI, dict, None],
)
async def get_road_data(request: Request, lat: float, lon: float):
    """
    Check headers using auth service and make response data
    :param request: info about request
    :param lat: tpi's latitude
    :param lon: tpi's longitude
    :return: str response of chatgpt or dict if chatgpt response status code != 200
    or error message of authenticate is failure
    """
    if request.headers.get("Authorization", None):
        token = request.headers["Authorization"]
        token_verification = await send_header_to_auth_service(token)
        match token_verification["status"]:
            case status.HTTP_200_OK:  # здесь бизнес логика по сбору данных
                weather = await processed_data_weather(lat, lon)
                message = await response_openai(weather, lat, lon)
                if message:
                    return message
                return weather
            case _:
                return JSONResponse(
                    status_code=token_verification["status"],
                    content=token_verification["message"],
                )
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "message": "provide an access token",
            },
        )
