import os
from unittest import mock
from unittest.mock import Mock, patch

from starlette import status

from src.analysis_road.collect_data import summing_result_road
from src.auth.check_auth import send_header_to_auth_service
from src.auth.crud_tpi import request_auth_create_tpi
from src.handlers.schemas import TPI
from src.open_ai.open_ai_response import response_openai
from src.utils import Url
from tests.fixture import (
    chat_gpt_response,
    headers,
    message_for_chatgpt,
    request_tpi_schemas,
    response_api,
    result_chatgpt,
    start_data,
    traffic_jams_good,
)


@patch("src.auth.crud_tpi.requests")
async def test_request_auth_create_tpi(mock_requests):
    mock_requests.post.return_value.status_code = status.HTTP_201_CREATED
    response = await request_auth_create_tpi(
        request_tpi_schemas, headers["Authorization"], 55.02, 22.201
    )
    assert response is True


@patch("src.auth.crud_tpi.requests")
async def test_request_auth_create_tpi_bad(mock_requests):
    mock_requests.post.return_value.status_code = status.HTTP_401_UNAUTHORIZED
    response = await request_auth_create_tpi(
        request_tpi_schemas, headers["Authorization"], 55.02, 22.201
    )
    assert response is False


@patch("src.auth.check_auth.requests")
async def test_send_header_to_auth_service(mock_requests):
    mock_response = {"lat_end": 55.37, "lon_end": 58.25}
    mock_requests.get.return_value.status_code = status.HTTP_200_OK
    mock_requests.get.return_value.json = Mock(return_value=mock_response)
    response = await send_header_to_auth_service(headers, request_tpi_schemas)
    assert response == {"lat_end": 55.37, "lon_end": 58.25}


async def test__convert_data_to_message_openai():
    from src.open_ai.open_ai_response import _convert_data_to_message_openai

    result = await _convert_data_to_message_openai(response_api)
    assert result == chat_gpt_response["message"]


async def test_response_openai():
    mock_response__convert_data_to_message_openai = mock.AsyncMock(
        return_value=message_for_chatgpt
    )
    mock__send_request_openai_chat_completion = mock.AsyncMock(
        return_value=result_chatgpt
    )
    with mock.patch(
        "src.open_ai.open_ai_response._convert_data_to_message_openai",
        mock_response__convert_data_to_message_openai,
    ), mock.patch(
        "src.open_ai.open_ai_response._send_request_openai_chat_completion",
        mock__send_request_openai_chat_completion,
    ):
        result = await response_openai(
            response_api, start_data["lat"], start_data["lon"]
        )
        assert result == result_chatgpt


async def test_url_weather():
    url = Url(lat=55, lon=37, count=1).weather
    assert url == (
        f"https://api.weather.yandex.ru/v2/forecast?"
        f"lat={55}"
        f"&lon={37}"
        f"&lang=ru_RU"
        f"&limit={1}"
        f"&hours=False"
        f"&extra=False"
    )


async def test_url_chat_gpt():
    url = Url().open_ai
    assert url == "https://api.openai.com/v1/chat/completions"


async def test_url_2gis():
    url = Url().to_gis
    assert (
        url
        == f"http://routing.api.2gis.com/routing/7.0.0/global?key={os.getenv('KEY_2GIS')}"
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
