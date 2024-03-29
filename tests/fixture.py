from starlette import status
from starlette.responses import JSONResponse

from src.handlers.schemas import TPI

start_data = {"lat": 54.4334, "lon": 55.5651}

stop_data = {"lat": 54.7431, "lon": 55.9678}

response_yandex_example = {
    "now": 1698234863,
    "now_dt": "2023-10-25T11:54:23.805001Z",
    "info": {
        "n": True,
        "geoid": 213,
        "url": "https://yandex.ru/pogoda/213?lat=55.75396&lon=37.620393",
        "lat": 55.75396,
        "lon": 37.620393,
        "tzinfo": {
            "name": "Europe/Moscow",
            "abbr": "MSK",
            "dst": False,
            "offset": 10800,
        },
        "def_pressure_mm": 747,
        "def_pressure_pa": 995,
        "slug": "213",
        "zoom": 10,
        "nr": True,
        "ns": True,
        "nsr": True,
        "p": False,
        "f": True,
        "_h": False,
    },
    "geo_object": {
        "district": {"id": 120540, "name": "Тверской район"},
        "locality": {"id": 213, "name": "Москва"},
        "province": {"id": 213, "name": "Москва"},
        "country": {"id": 225, "name": "Россия"},
    },
    "yesterday": {"temp": 2},
    "fact": {
        "obs_time": 1698234863,
        "uptime": 1698234863,
        "temp": 0,
        "feels_like": -4,
        "icon": "bkn_d",
        "condition": "cloudy",
        "cloudness": 0.5,
        "prec_type": 0,
        "prec_prob": 0,
        "prec_strength": 0,
        "is_thunder": False,
        "wind_speed": 1.6,
        "wind_dir": "e",
        "pressure_mm": 750,
        "pressure_pa": 999,
        "humidity": 52,
        "daytime": "d",
        "polar": False,
        "season": "autumn",
        "source": "station",
        "accum_prec": {"3": 9.130245, "7": 28.826782, "1": 0},
        "soil_moisture": 0.38,
        "soil_temp": 4,
        "uv_index": 1,
        "wind_gust": 3.9,
    },
    "forecasts": [
        {
            "date": "2023-10-25",
            "date_ts": 1698181200,
            "week": 43,
            "sunrise": "07:19",
            "sunset": "17:07",
            "rise_begin": "06:41",
            "set_end": "17:45",
            "moon_code": 14,
            "moon_text": "moon-code-14",
            "parts": {
                "night": {
                    "_source": "0,1,2,3,4,5",
                    "temp_min": -1,
                    "temp_avg": 0,
                    "temp_max": 0,
                    "wind_speed": 1.4,
                    "wind_gust": 4.1,
                    "wind_dir": "n",
                    "pressure_mm": 749,
                    "pressure_pa": 998,
                    "humidity": 77,
                    "soil_temp": 2,
                    "soil_moisture": 0.38,
                    "prec_mm": 0.6,
                    "prec_prob": 20,
                    "prec_period": 360,
                    "cloudness": 1,
                    "prec_type": 3,
                    "prec_strength": 0.25,
                    "icon": "ovc_-sn",
                    "condition": "light-snow",
                    "uv_index": 0,
                    "feels_like": -3,
                    "daytime": "n",
                    "polar": False,
                    "fresh_snow_mm": 0,
                },
                "morning": {
                    "_source": "6,7,8,9,10,11",
                    "temp_min": -1,
                    "temp_avg": -1,
                    "temp_max": 0,
                    "wind_speed": 1.4,
                    "wind_gust": 4.1,
                    "wind_dir": "ne",
                    "pressure_mm": 750,
                    "pressure_pa": 999,
                    "humidity": 73,
                    "soil_temp": 1,
                    "soil_moisture": 0.38,
                    "prec_mm": 0.3,
                    "prec_prob": 20,
                    "prec_period": 360,
                    "cloudness": 1,
                    "prec_type": 3,
                    "prec_strength": 0.25,
                    "icon": "ovc_-sn",
                    "condition": "light-snow",
                    "uv_index": 1,
                    "feels_like": -5,
                    "daytime": "d",
                    "polar": False,
                    "fresh_snow_mm": 0.3,
                },
                "day": {
                    "_source": "12,13,14,15,16,17",
                    "temp_min": -1,
                    "temp_avg": 0,
                    "temp_max": 1,
                    "wind_speed": 1.7,
                    "wind_gust": 4.5,
                    "wind_dir": "e",
                    "pressure_mm": 750,
                    "pressure_pa": 999,
                    "humidity": 56,
                    "soil_temp": 3,
                    "soil_moisture": 0.37,
                    "prec_mm": 0,
                    "prec_prob": 0,
                    "prec_period": 360,
                    "cloudness": 0.5,
                    "prec_type": 0,
                    "prec_strength": 0,
                    "icon": "bkn_d",
                    "condition": "cloudy",
                    "uv_index": 1,
                    "feels_like": -4,
                    "daytime": "d",
                    "polar": False,
                    "fresh_snow_mm": 0,
                },
                "evening": {
                    "_source": "18,19,20,21",
                    "temp_min": -1,
                    "temp_avg": -1,
                    "temp_max": 0,
                    "wind_speed": 1.5,
                    "wind_gust": 3.2,
                    "wind_dir": "e",
                    "pressure_mm": 750,
                    "pressure_pa": 999,
                    "humidity": 70,
                    "soil_temp": 1,
                    "soil_moisture": 0.37,
                    "prec_mm": 0.1,
                    "prec_prob": 20,
                    "prec_period": 240,
                    "cloudness": 0.75,
                    "prec_type": 3,
                    "prec_strength": 0.25,
                    "icon": "bkn_-sn_n",
                    "condition": "light-snow",
                    "uv_index": 0,
                    "feels_like": -5,
                    "daytime": "n",
                    "polar": False,
                    "fresh_snow_mm": 0.1,
                },
                "day_short": {
                    "_source": "6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21",
                    "temp": 1,
                    "temp_min": -1,
                    "wind_speed": 1.7,
                    "wind_gust": 4.5,
                    "wind_dir": "e",
                    "pressure_mm": 750,
                    "pressure_pa": 999,
                    "humidity": 66,
                    "soil_temp": 1,
                    "soil_moisture": 0.38,
                    "prec_mm": 0.4,
                    "prec_prob": 20,
                    "prec_period": 960,
                    "cloudness": 0.75,
                    "prec_type": 3,
                    "prec_strength": 0.25,
                    "icon": "bkn_-sn_d",
                    "condition": "light-snow",
                    "uv_index": 1,
                    "feels_like": -4,
                    "daytime": "d",
                    "polar": False,
                    "fresh_snow_mm": 0,
                },
                "night_short": {
                    "_source": "0,1,2,3,4,5",
                    "temp": -1,
                    "wind_speed": 1.4,
                    "wind_gust": 4.1,
                    "wind_dir": "n",
                    "pressure_mm": 749,
                    "pressure_pa": 998,
                    "humidity": 77,
                    "soil_temp": 2,
                    "soil_moisture": 0.38,
                    "prec_mm": 0.6,
                    "prec_prob": 20,
                    "prec_period": 360,
                    "cloudness": 1,
                    "prec_type": 3,
                    "prec_strength": 0.25,
                    "icon": "ovc_-sn",
                    "condition": "light-snow",
                    "uv_index": 0,
                    "feels_like": -3,
                    "daytime": "n",
                    "polar": False,
                    "fresh_snow_mm": 0,
                },
            },
            "hours": [],
            "biomet": {"index": 0, "condition": "magnetic-field_0"},
        },
    ],
}

response_api = {
    "city": "Москва",
    "temperature": 0,
    "feels_like": -4,
    "condition": "cloudy",
    "pressure_mm": 750,
    "pressure_pa": 999,
    "humidity": 52,
    "wind_gust": 3.9,
}

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJ1c2VyX2lkIjoiMTIiLCJleHAiOjE3MDEzMzE1MTAsImlhdCI6MTY5ODczOTUxMH0."
    "_Pw9fLsSwcRx4Ie3fe0L7EHC7Vz9u6MkXlpBSu7o_rI",
}

headers_bad = {
    "Authorization": "Bearer eyJhbGciOiJIU123123zI1NiIsInR5cCI6IkpXVCJ9."
    "eyJ1c2VyX2lkIjoiMTIiLCJleHAiOjE3MDEzMzE1MTAsImlhdCI6MTY5ODczOTUxMH0."
    "_Pw9fLsSwcRx4Ie3fe0L7EHC7Vz9u6MkXlpBSu7o_rI",
}

request_tpi_schemas = TPI(
    lat_start=55.0,
    lon_start=37.0,
    start="Вологда",
    end="Москва",
    highway="m8",
)

request_tpi_without_schemas = {
    "lat_start": 55.0,
    "lon_start": 37.0,
    "start": "Вологда",
    "end": "Москва",
    "highway": "m8",
}
mock_response_bad = {
    "message": {
        "detail": "Недействительный токен доступа",
    },
    "status": status.HTTP_403_FORBIDDEN,
}

chat_gpt_response = {
    "message": "Из приведенных данных проведи анализ погодных условий и сделай вывод о возможности гололеда и других не благоприятных условиях для водителя (туман и другие), информация должна быть краткой и понятной, если есть опасные погодные условия написать их капсом. На основе этих данных дай информацию и рекомендации для водителей двигающихся по трассе, информация должна быть краткой и понятной. На основе анализа погоды так же составь сообщения которые требуется вывести на табло переменной информации в соответствии с гостом ГОСТ Р 56351—201 и ГОСТ Р 56350—2015 Российской Федерации. city: Москва temperature: 0 feels_like: -4 condition: cloudy pressure_mm: 750 pressure_pa: 999 humidity: 52 wind_gust: 3.9 "
}

auth_service_response = {
    "lat_end": 55.37,
    "lon_end": 54.21,
}

auth_service_response_failure = False

message_for_chatgpt = (
    "Из приведенных данных проведи анализ погодных условий и"
    " сделай вывод о возможности гололеда и других не благоприятных"
    " условиях для водителя (туман и другие), информация должна быть краткой и понятной,"
    " если есть опасные погодные условия написать их капсом."
    " На основе этих данных дай информацию и"
    " рекомендации для водителей двигающихся по трассе, информация должна быть краткой и понятной."
    " На основе анализа погоды так же составь сообщения "
    "которые требуется вывести на табло переменной информации"
    "в соответсвии с гостом ГОСТ Р 56351—201 и ГОСТ Р 56350—2015 Российской Федерации."
)

result_chatgpt = (
    "city: Москва temperature: 0 feels_like: -4 condition: cloudy pressure_mm: 750"
    " pressure_pa: 999 humidity: 52 wind_gust: 3.9"
)
result_chatgpt_status_code_200 = JSONResponse(
    status_code=status.HTTP_200_OK,
    content=chat_gpt_response["message"],
)

result_chatgpt_bad = JSONResponse(
    status_code=status.HTTP_400_BAD_REQUEST,
    content="error",
)

result_chatgpt_status_code_400 = JSONResponse(
    status_code=status.HTTP_400_BAD_REQUEST,
    content="error",
)

traffic_jams_good = {"duration": 5450, "length": 5400, "status_of_jams": 4}
traffic_jams = {"duration": 5450, "length": 5400}
for_2gis_req = {
    "lat_start": 55.0,
    "lon_start": 37.0,
    "lat_end": 55.37,
    "lon_end": 54.21,
}

response_2gis_api = {
    "result": [{"duration": 5450, "length": 5400, "status_of_jams": 4}],
    "status": "OK",
}

response_2gis_api_bad_status = {
    "result": [{"duration": 5450, "length": 5400, "status_of_jams": 4}],
    "status": "Bad",
}
