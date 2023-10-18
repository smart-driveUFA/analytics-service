from fastapi import FastAPI, APIRouter

app = FastAPI(
    docs_url="/",
)

main_router = APIRouter(prefix="/analytic/v1")
