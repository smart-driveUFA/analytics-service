from fastapi import APIRouter, status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.analysis_road.collect_data import summing_result_road
from src.auth.check_auth import send_header_to_auth_service
from src.auth.crud_tpi import request_auth_create_tpi
from src.auth.send_result_data import send_result_auth
from src.database.mongo import client_mongo
from src.handlers.schemas import TPI, SummingData
from src.search_coordinates.search_end_coor import find_coordinates_end_of_highway

router = APIRouter(
    prefix="/routers",
    tags=["router_api"],
)


@router.post("/create-tpi", response_class=JSONResponse)
async def create_tpi(request: Request, tpi_data: TPI) -> JSONResponse:
    """
    Accepts the request to create tpi with params
    :param request: info about request
    :param tpi_data: schema of data
    :return:
    """
    if request.headers.get("Authorization", None):
        (
            coordinates_end_lat,
            coordinates_end_lon,
        ) = await find_coordinates_end_of_highway(
            tpi_data.lat_start, tpi_data.lon_start, tpi_data.end
        )
        tpi_response = await request_auth_create_tpi(
            tpi_data,
            request.headers["Authorization"],
            coordinates_end_lat,
            coordinates_end_lon,
        )
        if tpi_response:
            if isinstance(tpi_response, dict) and tpi_response.get("detail", None):
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST, content=tpi_response
                )
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
async def collect_road_data(request: Request, route_coor: TPI):
    """
    check authentication and process road data
    :param request: info about request for check authentication
    :param route_coor: coordinate parameters start and stop location
    :return: SummingData weather, recommended message and traffic jams status and
    coordinates of tpi or unauthorized status
    """
    if request.headers.get("Authorization", None):
        token = request.headers["Authorization"]
        coor_end_point = await send_header_to_auth_service(token, route_coor)
        if coor_end_point.get("lat_end", None) and coor_end_point.get("lon_end", None):
            result_process = await summing_result_road(
                route_coor, coor_end_point["lat_end"], coor_end_point["lon_end"]
            )
            result_process.pop("_id", None)
            await send_result_auth(
                result_process, token, route_coor.lat_start, route_coor.lon_start
            )
            result_process.pop("lat", None)
            result_process.pop("lon", None)
            return result_process
        elif coor_end_point.get("detail", None):
            return JSONResponse(
                status_code=coor_end_point["status_code"],
                content={
                    "message": coor_end_point["detail"],
                },
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
