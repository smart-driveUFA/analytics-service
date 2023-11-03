from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.auth.crud_tpi import request_auth_create_tpi
from src.handlers.schemas import CreateTPI
from src.yandex_api.schemas import ResponseAPI

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
    headers = {
        "Authorization": request.headers["Authorization"],
    }
    tpi_response = await request_auth_create_tpi(
        tpi_data.lat,
        tpi_data.lon,
        tpi_data.direction,
        headers,
    )
    return JSONResponse(
        status_code=tpi_response["status"],
        content=tpi_response["message"],
    )
