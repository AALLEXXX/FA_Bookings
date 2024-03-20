from datetime import date

from sqlalchemy import func, select, text
from sqlalchemy.orm import aliased

from app.bookings.bookings_model import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.hotels_model import Hotels
from app.hotels.rooms.rooms_model import Rooms


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all(
        cls,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        """
        select h.id as hotel_id,
                r.name as room_name,
                r.description,
                jsonb_agg(r.services) AS services,
                r.price,
                r.quantity,
                r.image_id,
                ('2023-03-10'::date - '2023-03-5'::date) * r.price AS total_cost,
                r.quantity - COALESCE(COUNT(b.id), 0) AS rooms_left
                from hotels h
                left join rooms r on r.hotel_id = 1
                left join bookings b on r.id = b.room_id
                        AND (b.date_to <= '2023-03-10'::date AND b.date_from >= '2023-03-05'::date)
                where h.id = 1
                group by
                                h.id, r.name, r.price, r.description,  r.quantity, r.image_id;
        """
        async with async_session_maker() as session:

            stmt = (
                select(
                    Hotels.id.label("hotel_id"),
                    Rooms.name.label("room_name"),
                    Rooms.description,
                    func.jsonb_agg(Rooms.services).label("services"),
                    Rooms.price,
                    Rooms.quantity,
                    Rooms.image_id,
                    ((date_to - date_from).days * Rooms.price).label("total_cost"),
                    (Rooms.quantity - func.coalesce(func.count(Bookings.id), 0)).label(
                        "rooms_left"
                    ),
                )
                .select_from(Hotels)
                .join(Rooms, Rooms.hotel_id == hotel_id, isouter=True)
                .join(
                    Bookings,
                    (Rooms.id == Bookings.room_id)
                    & (
                        (Bookings.date_to <= date_to)
                        & (Bookings.date_from >= date_from)
                    ),
                    isouter=True,
                )
                .filter(Hotels.id == hotel_id)
                .group_by(
                    Hotels.id,
                    Rooms.name,
                    Rooms.price,
                    Rooms.description,
                    Rooms.quantity,
                    Rooms.image_id,
                )
            )

            result = await session.execute(stmt)
            return result.mappings().all()
