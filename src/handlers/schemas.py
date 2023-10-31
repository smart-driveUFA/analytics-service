from pydantic import BaseModel


class CreateTPI(BaseModel):
    lat: float
    lon: float
    direction: str
    count: int
