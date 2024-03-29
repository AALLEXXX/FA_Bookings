from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.hotels import get_hotels
from app.api.users import login_user
from app.schemas.users import SUserRegister

router = APIRouter(tags=["Фронтентд"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels")
async def get_hotels_page(request: Request, hotels=Depends(get_hotels)):
    return templates.TemplateResponse(
        name="hotels.html", context={"request": request, "hotels": hotels}
    )


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(
    request: Request,
):
    return templates.TemplateResponse("auth.html", {"request": request})


@router.post("/ok")
async def handle_login(
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    user: SUserRegister = Depends(login_user),
):
    return (email, password)
