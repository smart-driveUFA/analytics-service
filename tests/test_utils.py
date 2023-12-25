import os

from src.utils import Url


async def test_url_chat_gpt():
    url = Url().open_ai
    assert url == "https://api.openai.com/v1/chat/completions"


async def test_url_2gis():
    url = Url().to_gis
    assert url == f"http://routing.api.2gis.com/routing/7.0.0/global?key={os.getenv('KEY_2GIS')}"


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
