from src.api_2gis.too_gis import status_road_speed
from src.database.mongo import client_mongo
from src.handlers.schemas import CoordinatesBetweenTPI
from src.open_ai.open_ai_response import response_openai
from src.yandex_api.weather_api import processed_data_weather


async def summing_result_road(route_coor: CoordinatesBetweenTPI):
    """
    collect data of road-to-response dict
    :param route_coor: coordinate parameters start and stop location
    :return: SummingData weather, recommended message and traffic jams status; someone can be None
    """
    weather = await processed_data_weather(route_coor.start.lat, route_coor.start.lon)
    if weather:
        weather.pop("_id", None)
        message = await response_openai(
            weather, route_coor.start.lat, route_coor.start.lon
        )
        traffic_jams_status = await status_road_speed(route_coor)
        analysis_data = {
            "weather": weather,
            "recommended_information": message,
            "road_traffic_status": traffic_jams_status,
        }
        client_mongo["summing_result"].insert_one(analysis_data)
        analysis_data.pop("_id", None)
        return analysis_data
    return None
