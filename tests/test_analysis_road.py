from unittest.mock import patch

from src.analysis_road.collect_data import summing_result_road
from src.handlers.schemas import TPI
from tests.fixture import (
    request_tpi_schemas,
    response_api,
    result_chatgpt,
    traffic_jams_good,
)


async def test_summing_result_road():
    with patch(
        "src.analysis_road.collect_data.processed_data_weather",
        return_value=response_api,
    ), patch(
        "src.analysis_road.collect_data.response_openai", return_value=result_chatgpt
    ), patch(
        "src.analysis_road.collect_data.status_road_speed",
        return_value=traffic_jams_good,
    ):
        coor = TPI.model_validate(request_tpi_schemas)
        result = await summing_result_road(coor, 0.0, 0.0)
        assert result == {
            "weather": response_api,
            "recommended_information": result_chatgpt,
            "traffic_jams_status": traffic_jams_good,
        }
