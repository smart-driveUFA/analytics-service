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
    analysis_data = {}
    weather = await processed_data_weather(route_coor.start.lat, route_coor.start.lon)
    if weather:
        weather.pop("_id", None)
        analysis_data["weather"] = weather
    message = await response_openai(weather, route_coor.start.lat, route_coor.start.lon)
    if message:
        analysis_data["recommended_information"] = message
    traffic_jams_status = await status_road_speed(route_coor)
    if traffic_jams_status:
        analysis_data["traffic_jams_status"] = traffic_jams_status
    client_mongo["summing_result"].insert_one(analysis_data)
    analysis_data.pop("_id", None)
    return analysis_data
