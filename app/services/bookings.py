from app.exeptions import RoomCannotBeBooked, RoomCannotBeDeleted
from app.models.users import Users
from app.schemas.bookings import SBookings
from app.tasks.tasks import send_booking_confirmation_email
from app.utils.repository import AbstractRepository


class BookingsService:
    def __init__(self, bookings_repo: AbstractRepository) -> None:
        self.bookings_repo = bookings_repo

    async def add_booking(self, new_booking: SBookings, user: Users):
        booking = await self.bookings_repo.add(
            user.id, new_booking.room_id, new_booking.date_from, new_booking.date_to
        )
        if not booking:
            raise RoomCannotBeBooked
        booking_dict = SBookings.model_validate(booking).model_dump()
        send_booking_confirmation_email.delay(booking_dict, user.email)

        return booking_dict

    async def get_user_bookings(self, user): 
        bookings: list[dict]= await self.bookings_repo.find_all(user_id=user.id)
        # bookings_dump = SBookings.model_validate(*bookings).model_dump() #TODO
        bookings_dump = [SBookings.model_validate(i).model_dump() for i in bookings]   
        return bookings_dump

    async def delete_booking(self, user, booking):
        result = await self.bookings_repo.delete_booking(
            booking.booking_id, user_id=user.id
        )
        if result:
            return "Successful"
        raise RoomCannotBeDeleted
