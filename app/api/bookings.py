from fastapi import APIRouter, Depends
from typing import List
from fastapi_versioning import version

from app.api.dependencies import get_bookings_service

from app.schemas.bookings import SBookings, SDeleteBooking, SNewBookings

from app.services.bookings import BookingsService

from app.api.dependencies import get_current_user
from app.models.users import Users
from app.utils.booking_util import validate_date

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
@version(1)
async def get_user_bookings(
    user: Users = Depends(get_current_user),
    bookins_service: BookingsService = Depends(get_bookings_service),
) -> List[SBookings]:
    bookings = await bookins_service.get_user_bookings(user)
    return bookings


@router.post("", status_code=201, dependencies=[Depends(validate_date)])
@version(1)
async def add_booking(
    new_booking: SNewBookings = Depends(),
    user: Users = Depends(get_current_user),
    bookins_service: BookingsService = Depends(get_bookings_service),
) -> SBookings:
    booking = await bookins_service.add_booking(new_booking, user)
    return booking


@router.delete("/{booking_id}", status_code=204)
@version(1)
async def delete_booking(
    booking: SDeleteBooking = Depends(),
    user: Users = Depends(get_current_user),
    bookins_service: BookingsService = Depends(get_bookings_service),
):
    await bookins_service.delete_booking(user=user, booking=booking)
