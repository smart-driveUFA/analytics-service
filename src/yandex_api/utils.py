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
        self.gpt = "https://llm.api.cloud.yandex.net/llm/v1alpha/instruct"
