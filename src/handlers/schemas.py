from typing import Union

from pydantic import BaseModel

from src.yandex_api.schemas import ResponseAPI


class GetDataCoordinates(BaseModel):
    lat_start: float
    lon_start: float


class EnterDirection(BaseModel):
    start: str
    end: str
    highway: str


class TPI(GetDataCoordinates, EnterDirection):
    pass


class TrafficQuantity(BaseModel):
    duration: int
    length: int
    status_of_jams: str


class SummingData(BaseModel):
    weather: Union[ResponseAPI, None]
    recommended_information: Union[str, None]
    traffic_jams_status: Union[TrafficQuantity, None]
