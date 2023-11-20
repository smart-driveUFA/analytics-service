import os
from typing import Optional


class Url:
    def __init__(
        self,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        count: Optional[int] = 1,
    ):
        self.weather = (
            f"https://api.weather.yandex.ru/v2/forecast?"
            f"lat={lat}"
            f"&lon={lon}"
            f"&lang=ru_RU"
            f"&limit={count}"
            f"&hours=False"
            f"&extra=False"
        )
        self.open_ai = "https://api.openai.com/v1/chat/completions"
        self.to_gis = f"http://routing.api.2gis.com/routing/7.0.0/global?key={os.getenv('KEY_2GIS')}"
