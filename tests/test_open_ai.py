from unittest import mock

from src.open_ai.open_ai_response import response_openai
from tests.fixture import (
    chat_gpt_response,
    message_for_chatgpt,
    response_api,
    result_chatgpt,
    start_data,
)


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


async def test__convert_data_to_message_openai():
    from src.open_ai.open_ai_response import _convert_data_to_message_openai

    result = await _convert_data_to_message_openai(response_api)
    assert result == chat_gpt_response["message"]
