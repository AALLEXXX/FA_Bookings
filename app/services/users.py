from fastapi import Request, Response
from app.api.auth import authenticate_user, create_access_token, get_password_hash
from app.exeptions import (
    CanntDeleteCookies,
    IncorrenctEmailOrPasswordExeption,
    UserAlreadyExistsExeption,
)
from app.schemas.users import SUserRegister
from app.utils.repository import AbstractRepository


class UsersService:
    def __init__(self, users_repo: AbstractRepository) -> None:
        self.users_repo = users_repo

    async def register_user(self, user_data: SUserRegister):
        existing_user = await self.users_repo.find_one_or_none(email=user_data.email)
        if existing_user:
            raise UserAlreadyExistsExeption
        hashed_password = get_password_hash(user_data.password)
        await self.users_repo.add(
            email=user_data.email, hashed_password=hashed_password
        )

    async def logout_user(self, request: Request, response: Response):
        if "booking_access_token" in request.cookies:
            return response.delete_cookie("booking_access_token")
        raise CanntDeleteCookies("Вы уже вышли из аккаунта")

    async def login_user(
        self, request: Request, response: Response, user_data: SUserRegister
    ):
        user = await authenticate_user(
            email=user_data.email, password=user_data.password
        )
        if not user:
            raise IncorrenctEmailOrPasswordExeption
        if "booking_access_token" in request.cookies:
            access_token = request.cookies["booking_access_token"]
            return access_token

        access_token = create_access_token({"sub": str(user.id)})
        response.set_cookie("booking_access_token", access_token, httponly=True)
        return access_token
