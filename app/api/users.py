from fastapi import APIRouter, Depends, Request, Response

from app.api.dependencies import get_users_service
from app.api.dependencies import get_current_user
from app.schemas.users import SUserMe, SUserRegister
from app.models.users import Users
from app.services.users import UsersService

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)


@router.post("/register")
async def register_user(
    user_data: SUserRegister, users_service: UsersService = Depends(get_users_service)
):
    return await users_service.register_user(user_data=user_data)


@router.post("/login")
async def login_user(
    request: Request,
    response: Response,
    user_data: SUserRegister,
    users_service: UsersService = Depends(get_users_service),
):
    return await users_service.login_user(
        request=request, response=response, user_data=user_data
    )


@router.post("/logout")
async def logout_user(
    request: Request,
    response: Response,
    users_service: UsersService = Depends(get_users_service),
):
    return await users_service.logout_user(request=request, response=response)


@router.post("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)) -> SUserMe:
    return current_user
