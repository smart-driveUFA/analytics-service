from fastapi import APIRouter, status
from starlette.requests import Request

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
    status_code=status.HTTP_201_CREATED,
)
async def create_tpi(request: Request, tpi_data: CreateTPI):
    headers = {
        "Authorization": request.headers["Authorization"],
    }
    headers_valid = await send_header_to_auth_service(headers)
    if headers_valid["status"] == status.HTTP_200_OK:
        tpi_response = await request_auth_create_tpi(
            tpi_data.lat, tpi_data.lon, tpi_data.direction, headers,
        )
        if tpi_response["status"] == status.HTTP_201_CREATED:
            return await get_weather(
                lat=tpi_data.lat,
                lon=tpi_data.lon,
                count=tpi_data.count,
            )
        else:
            return tpi_response
    return headers_valid
