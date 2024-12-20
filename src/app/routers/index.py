"""Hi
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import Request
from app.dependencies import templates


router = APIRouter(
    prefix="",
    tags=["index"],
    dependencies=[],
    responses={404: {"message": "Not found", "code": 404}},
)


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("fe3.html", {"request": request, "data": 10})
