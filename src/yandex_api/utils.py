class Url:
    def __init__(self, lat, lon, count):
        self.url = (
            f"https://api.weather.yandex.ru/v2/forecast?"
            f"lat={lat}"
            f"&lon={lon}"
            f"&lang=ru_RU"
            f"&limit={count}"
            f"&hours=False"
            f"&extra=False"
        )
