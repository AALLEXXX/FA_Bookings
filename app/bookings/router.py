from datetime import date
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookings, SDeleteBooking, SNewBookings
from app.users.dependencies import get_current_user
from app.users.user_model import Users
from fastapi import APIRouter, Depends
from app.bookings.bookings_model import Bookings
from app.exeptions import RoomCannotBeBooked
from app.bookings.schemas import SBookings
from app.tasks.tasks import send_booking_confirmation_email


router = APIRouter(
    prefix= "/bookings",
    tags=['Бронирования'],
)

@router.get('')
async def get_user_bookings(user: Users = Depends(get_current_user)):
    return await BookingDAO.find_all(user_id=user.id)




@router.post('')
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user)
    ):

    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking_dict = SBookings.model_validate(booking).model_dump()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict
    

@router.delete('/{booking_id}')
async def delete_booking( booking : SDeleteBooking = Depends(), 
    user: Users = Depends(get_current_user)):
    result = await BookingDAO.delete_booking(booking.booking_id, user_id=user.id)
    return result