from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI

from src.handlers.router import router as main_router_api
load_dotenv()

app = FastAPI(
    docs_url="/",
)

main_router = APIRouter(prefix="/smart-drive/v1")
main_router.include_router(main_router_api)
app.include_router(main_router)
