from fastapi import APIRouter, status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.analysis_road.collect_data import summing_result_road
from src.auth.check_auth import send_header_to_auth_service
from src.auth.crud_tpi import request_auth_create_tpi
from src.database.mongo import client_mongo
from src.handlers.schemas import CoordinatesBetweenTPI, CreateTPI, SummingData

router = APIRouter(
    prefix="/routers",
    tags=["router_api"],
)


@router.post("/create-tpi", response_class=JSONResponse)
async def create_tpi(request: Request, tpi_data: CreateTPI) -> JSONResponse:
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
        if tpi_response:
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "message": "successfully created",
                },
            )
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "message": "check Authorization token, and try again",
            },
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "message": "check Authorization token, and try again",
            },
        )


@router.post("/traffic-status", response_model=SummingData, response_class=JSONResponse)
async def collect_road_data(request: Request, route_coor: CoordinatesBetweenTPI):
    """
    check authentication and process road data
    :param request: info about request for check authentication
    :param route_coor: coordinate parameters start and stop location
    :return: SummingData weather, recommended message and traffic jams status or unauthorized status
    """
    if request.headers.get("Authorization", None):
        token = request.headers["Authorization"]
        token_verification = await send_header_to_auth_service(
            token, route_coor.start.lat, route_coor.start.lon
        )
        if token_verification:
            return await summing_result_road(  # здесь бизнес логика по сбору данных
                route_coor
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "message": "check Authorization token, and try again",
                },
            )
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "message": "check Authorization token, and try again",
            },
        )


@router.delete("/delete-collection")
async def delete_collection_mongodb(name: str):
    await client_mongo[name].delete_many({})
    return {"message": f"successfully delete {name} collection"}
