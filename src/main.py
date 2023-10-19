from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI

from src.yandex_api.weather_api import router as yandex_router

load_dotenv()

app = FastAPI(
    docs_url="/",
)

main_router = APIRouter(prefix="/analytic/v1")
main_router.include_router(yandex_router)
app.include_router(main_router)
