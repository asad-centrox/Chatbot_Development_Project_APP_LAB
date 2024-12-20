"""Hi!
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.dependencies import templates

import os

router = APIRouter(
    prefix="/chatbot_interface",
    tags=["chatbot_interface"],
    dependencies=[],
    responses={404: {"message": "Not found", "code": 404}},
)


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "fe3.html",
        {"request": request, "url": os.environ.get("FE")},
    )
