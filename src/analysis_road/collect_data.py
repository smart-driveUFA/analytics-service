from src.api_2gis.too_gis import status_road_speed
from src.database.mongo import client_mongo
from src.handlers.schemas import TPI
from src.open_ai.open_ai_response import response_openai
from src.yandex_api.weather_api import processed_data_weather


async def summing_result_road(route_coor: TPI, lat_end: float, lon_end: float):
    """
    collect data of road-to-response dict
    :param lon_end:
    :param lat_end:
    :param route_coor: coordinate parameter start location
    :return: SummingData weather, recommended message and traffic jams status; someone can be None
    """

    weather = await processed_data_weather(route_coor.lat_start, route_coor.lon_start)
    if weather:
        weather.pop("_id", None)
    message = await response_openai(weather, route_coor.lat_start, route_coor.lon_start)
    traffic_jams_status = await status_road_speed(
        route_coor.lat_start, route_coor.lon_start, lat_end, lon_end
    )
    if traffic_jams_status:
        traffic_jams_status.pop("_id", None)
    analysis_data = {
        "weather": weather,
        "recommended_information": message,
        "traffic_jams_status": traffic_jams_status,
    }
    client_mongo["summing_result"].insert_one(analysis_data)
    analysis_data.pop("_id", None)
    return analysis_data
