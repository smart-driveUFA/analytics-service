import os
from math import atan2, degrees

from dadata import DadataAsync
from geopy import Point, distance

from src.exceptions.custom_exceptions import VariableError
from src.utils import city_russian_set


async def find_coordinates_end_of_highway(
    lat: float, lon: float, end: str, km: int = 50
):
    """
    computing coordinates end point route in 50 km;
    :param km: distance from tpi to end point route;
    :param lat: latitude of tpi;
    :param lon: longitude of tpi;
    :param end: name city of end or start highway;
    :return: tuple (lat, lon) of end point;
    """
    token_dadata = os.getenv("DADATA_KEY")
    secret_dadata = os.getenv("DADATA_SECRET_KEY")
    if token_dadata and secret_dadata:
        if isinstance(end, str) and end in city_russian_set:
            async with DadataAsync(token_dadata, secret_dadata) as dadata:
                coordinates_end = await dadata.clean(name="address", source=end)
                end_point = {
                    "lat": float(coordinates_end["geo_lat"]),
                    "lon": float(coordinates_end["geo_lon"]),
                }
                angle = degrees(atan2(end_point["lat"] - lat, end_point["lon"] - lon))
                destination_point = distance.geodesic(kilometers=km).destination(
                    Point(latitude=lat, longitude=lon), angle
                )
                return destination_point.latitude, destination_point.longitude
        else:
            raise TypeError("provided unexpected type")
    else:
        raise VariableError("provide token_data or secret_dadata")
