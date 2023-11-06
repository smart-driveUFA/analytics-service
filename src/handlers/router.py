from fastapi import APIRouter, status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.auth.check_auth import send_header_to_auth_service
from src.auth.crud_tpi import request_auth_create_tpi
from src.handlers.schemas import CreateTPI
from src.yandex_api.schemas import ResponseAPI
from src.yandex_api.weather_api import get_weather

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
    response_model=ResponseAPI | dict,
)
async def get_road_data(request: Request, lat: float, lon: float):
    """
    Check headers using auth service and make response data
    :param request: info about request
    :param lat: tpi's latitude
    :param lon: tpi's longitude
    :return: dict ResponseAPI or error message
    """
    if request.headers.get("Authorization", None):
        bearer = request.headers["Authorization"]
        token_verification = await send_header_to_auth_service(bearer)
        match token_verification["status"]:
            case status.HTTP_200_OK:
                return await get_weather(
                    lat=lat, lon=lon
                )  # здесь должна быть бизнес логика по сбору данных
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
