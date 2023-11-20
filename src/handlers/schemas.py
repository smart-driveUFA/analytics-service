from typing import Union

from pydantic import BaseModel

from src.yandex_api.schemas import ResponseAPI


class GetDataCoordinates(BaseModel):
    lat: float
    lon: float


class CreateTPI(GetDataCoordinates):
    direction: str
    count: int


class CoordinatesBetweenTPI(BaseModel):
    start: GetDataCoordinates
    stop: GetDataCoordinates


class TrafficQuantity(BaseModel):
    duration: int
    length: int
    status_of_jams: str


class SummingData(BaseModel):
    weather: Union[ResponseAPI, None]
    recommended_information: Union[str, None]
    road_traffic_status: Union[TrafficQuantity, None]
