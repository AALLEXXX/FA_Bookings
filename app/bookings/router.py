from datetime import date

from fastapi import APIRouter, Depends
from typing import Any, List
from fastapi_versioning import version
from pydantic import BaseModel

from app.bookings.bookings_model import Bookings
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookings, SDeleteBooking, SNewBookings
from app.exeptions import IncorrectDateForBooking, RoomCannotBeBooked, RoomCannotBeDeleted
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.user_model import Users
from app.utils.booking_util import validate_date

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
@version(1)
async def get_user_bookings(
    user: Users = Depends(get_current_user)
    ) -> List[SBookings]:
    return await BookingDAO.find_all(user_id=user.id)

        
@router.post("", status_code=201, dependencies=[Depends(validate_date)])
@version(1)
async def add_booking(
    new_booking: SNewBookings = Depends(),
    user: Users = Depends(get_current_user),
) -> SBookings: 
    booking = await BookingDAO.add(user.id, 
                                   new_booking.room_id, 
                                   new_booking.date_from, 
                                   new_booking.date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking_dict = SBookings.model_validate(booking).model_dump()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict


@router.delete("/{booking_id}", status_code=204)
@version(1)
async def delete_booking(
    booking: SDeleteBooking = Depends(), 
    user: Users = Depends(get_current_user)
): #TODO
    result = await BookingDAO.delete_booking(booking.booking_id, user_id=user.id)
    if result:
        return 'Successful'
    raise RoomCannotBeDeleted

