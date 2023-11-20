from typing import Union

from fastapi import APIRouter, status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.analysis_road.collect_data import summing_result_road
from src.auth.check_auth import send_header_to_auth_service
from src.auth.crud_tpi import request_auth_create_tpi
from src.database.mongo import client_mongo
from src.handlers.schemas import CoordinatesBetweenTPI, CreateTPI, SummingData
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


@router.post(
    "/traffic-status",
    response_model=Union[SummingData, dict, None],
)
async def collect_road_data(request: Request, route_coor: CoordinatesBetweenTPI):
    """
    check authentication and process road data
    :param request: info about request for check authentication
    :param route_coor: coordinate parameters start and stop location
    :return: SummingData weather, recommended message and traffic jams status or unauthorized status
    """
    if request.headers.get("Authorization", None):
        token = request.headers["Authorization"]
        token_verification = await send_header_to_auth_service(token)
        match token_verification["status"]:
            case status.HTTP_200_OK:
                return await summing_result_road(
                    route_coor
                )  # здесь бизнес логика по сбору данных
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


@router.delete("/delete-collection")
async def delete_collection_mongodb(name: str):
    await client_mongo[name].delete_many({})
    return {"message": f"successfully delete {name} collection"}
