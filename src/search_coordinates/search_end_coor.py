import os
from math import atan2, degrees
from typing import Union

import httpx
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
    name_city = await is_valid_city_name(end)
    token_dadata = os.getenv("DADATA_KEY")
    secret_dadata = os.getenv("DADATA_SECRET_KEY")
    if token_dadata and secret_dadata:
        if isinstance(name_city, str):
            try:
                async with DadataAsync(token_dadata, secret_dadata) as dadata:
                    coordinates_end = await dadata.clean(
                        name="address", source=name_city
                    )
                    end_point = {
                        "lat": float(coordinates_end["geo_lat"]),
                        "lon": float(coordinates_end["geo_lon"]),
                    }
                    angle = degrees(
                        atan2(end_point["lat"] - lat, end_point["lon"] - lon)
                    )
                    destination_point = distance.geodesic(kilometers=km).destination(
                        Point(latitude=lat, longitude=lon), angle
                    )
                    return destination_point.latitude, destination_point.longitude
            except httpx.HTTPStatusError:
                return None, None
        else:
            return None, None
    else:
        raise VariableError("provide token_data or secret_dadata")


async def is_valid_city_name(name: str) -> Union[str, None]:
    """
    check string to valid and exist in set city russia;
    :param name: name of city;
    :return: str if city exists in set city russia or none;
    """
    valid_letter = "абвгдежзийклмнопрстуфхцчшщъыьэю "
    name = name.strip().lower()
    if len(name) <= 1:
        return None
    for el in name:
        if el not in valid_letter:
            return None
    name = name.capitalize()
    if name.count(" ") > 1:
        return None
    if name in city_russian_set:
        return name
    return None
