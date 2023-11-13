from http import HTTPStatus
from unittest import mock
from unittest.mock import MagicMock, patch

from src.auth.check_auth import send_header_to_auth_service
from src.auth.crud_tpi import request_auth_create_tpi
from src.open_ai.open_ai_response import (
    _convert_data_to_message_openai,
    response_openai,
)
from src.utils import Url
from tests.fixture import (
    data,
    headers,
    message_for_chatgpt,
    response_api,
    result_chatgpt,
)


@patch("src.auth.crud_tpi.requests")
async def test_request_auth_create_tpi(mock_requests):
    mock_response_auth = MagicMock()
    mock_response_auth.status_code = 201
    mock_response_auth.json.return_value = {
        "message": "tpi created successfully",
    }
    mock_requests.post.return_value = mock_response_auth
    response = await request_auth_create_tpi(
        data["lat"],
        data["lon"],
        "Volgograd",
        headers,
    )
    assert response["status"] == HTTPStatus.CREATED
    assert response["message"] == {
        "message": "tpi created successfully",
    }


@patch("src.auth.check_auth.requests")
async def test_send_header_to_auth_service(mock_requests):
    mock_response_auth = MagicMock()
    mock_response_auth.status_code = 200
    mock_response_auth.json.return_value = {
        "message": "created",
        "status": 201,
    }
    mock_requests.post.return_value = mock_response_auth
    response = await send_header_to_auth_service(headers)
    assert response["status"] == HTTPStatus.OK
    assert response["message"] == {
        "message": "created",
        "status": 201,
    }


async def test__convert_data_to_message_openai():
    result = await _convert_data_to_message_openai(response_api)
    assert result == message_for_chatgpt


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
        result = await response_openai(response_api)
        assert result == result_chatgpt


async def test_response_openai_failure():
    mock_response__convert_data_to_message_openai = mock.AsyncMock(
        return_value=message_for_chatgpt
    )
    mock__send_request_openai_chat_completion = mock.AsyncMock(return_value=None)
    with mock.patch(
        "src.open_ai.open_ai_response._convert_data_to_message_openai",
        mock_response__convert_data_to_message_openai,
    ), mock.patch(
        "src.open_ai.open_ai_response._send_request_openai_chat_completion",
        mock__send_request_openai_chat_completion,
    ):
        result = await response_openai(response_api)
        assert result is None


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
