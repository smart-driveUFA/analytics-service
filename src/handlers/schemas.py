from pydantic import BaseModel


class GetDataCoordinates(BaseModel):
    lat: float
    lon: float


class CreateTPI(GetDataCoordinates):
    direction: str
    count: int
