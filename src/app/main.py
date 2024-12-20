"""Hi

"""

import os
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from utils import get_logger
from app.routers import index
from app.routers.api import user
from app.routers.api import index as api_index
from app.routers import fe
from app.routers.api import app as bot

logger = get_logger("main")

description = """
Hi

"""

app = FastAPI(
    title="AI Template",
    description=description,
    version="0.0.1",
    docs_url="/api/docs",
    redoc_url="/api/redocs",
)


def apply_origins(application: FastAPI):
    origins = os.getenv("ORIGINS", "*")
    origins_lst = origins.split(",")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins_lst,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return origins


origins_applied = apply_origins(app)
app.mount("/public", StaticFiles(directory="../public"), name="public")

logger.info(f"Accepting requests from origins {origins_applied}")

app.include_router(index.router)
app.include_router(fe.router)

api_v1_router = APIRouter(
    prefix="/api/v1",
    tags=[],
    dependencies=[],
    responses={404: {"message": "Not found", "code": 404}},
)
api_v1_router.include_router(api_index.router)
api_v1_router.include_router(user.router)
api_v1_router.include_router(bot.router)

app.include_router(api_v1_router)
