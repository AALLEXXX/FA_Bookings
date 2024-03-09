from datetime import date
from app.database import async_session_maker
from sqlalchemy import func, select
from app.dao.base import BaseDAO

from app.bookings.bookings_model import Bookings 
from app.hotels.hotels_model import Hotels 
from app.hotels.rooms.rooms_model import Rooms



class HotelDAO(BaseDAO):
    model = Hotels
    @classmethod
    async def find_all(
        cls,
        location: str,
        date_from: date,
        date_to: date
        ):
        """
        SELECT
            h.id AS hotel_id,
            h.name,
            h.location, 
            h.services,
            h.image_id,
            h.rooms_quantity AS total_rooms,
            h.rooms_quantity - COALESCE(COUNT(b.id), 0) AS available_rooms
        FROM
            hotels h
        LEFT JOIN
            rooms r ON h.id = r.hotel_id
        LEFT JOIN
            bookings b ON r.id = b.room_id
                    AND (b.date_from <= '2023-03-05' AND b.date_to >= '2023-03-06')
        WHERE h.location like '%Алтай%'
        GROUP BY
            h.id, h.rooms_quantity;
        """
        async with async_session_maker() as session:
            stmt = (
            select(
                Hotels.id.label('hotel_id'),
                Hotels.name,
                Hotels.location,
                Hotels.services,
                Hotels.image_id,
                Hotels.rooms_quantity.label('total_rooms'),
                (Hotels.rooms_quantity - func.coalesce(func.count(Bookings.id), 0)).label('available_rooms')
                        )
                    .select_from(Hotels)
                    .join(Rooms, Hotels.id == Rooms.id, isouter=True)
                    .join(Bookings, (Rooms.id == Bookings.room_id) & (Bookings.date_from <= date_from) & (Bookings.date_to >= date_to), isouter=True)
                    .filter(Hotels.location.like(f'%{location.capitalize().strip()}%'))
                    .group_by(Hotels.id, Hotels.rooms_quantity)
                )
            result = await session.execute(stmt)
            result = result.mappings().all()

            return result
        