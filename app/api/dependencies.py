from datetime import datetime

from fastapi import Depends, Request
from jose import JWSError, jwt

from app.config import settings
from app.exeptions import (
    IncorrenctTokenFormatExeption,
    TokenAbsentExeption,
    TokenExpiredExeption,
    UserIsNotPresentExeption,
)
from app.repositories.users import UserRepository


from app.repositories.bookings import BookingsRepository
from app.repositories.hotels import HotelsRepository
from app.repositories.rooms import RoomsRepository
from app.repositories.users import UserRepository
from app.services.bookings import BookingsService
from app.services.hotels import HotelsService
from app.services.rooms import RoomsService
from app.services.users import UsersService


def get_bookings_service():
    return BookingsService(BookingsRepository)

def get_hotels_service():
    return HotelsService(HotelsRepository)

def get_rooms_service():
    return RoomsService(RoomsRepository)

def get_users_service():
    return UsersService(UserRepository)


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentExeption
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWSError:
        raise IncorrenctTokenFormatExeption

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredExeption

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentExeption

    user = await UserRepository.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentExeption
    return user
