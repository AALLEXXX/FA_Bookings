from app.bookings.bookings_model import Bookings
from app.hotels.rooms.rooms_model import Rooms
from datetime import date
from app.dao.base import BaseDAO
from sqlalchemy import and_, delete, func, insert, or_, select
from app.database import async_session_maker



class BookingDAO(BaseDAO):
    model = Bookings
    @classmethod
    async def get_rooms_left(
        cls,
        session,
        room_id: int,
        date_from: date,
        date_to: date
    ):
        """
        WITH booked_rooms AS (
        SELECT * FROM bookings
        WHERE room_id = 1 AND 
            (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
            (date_from <= '2023-05-15' AND date_to > '2023-05-15')
            )
        SELECT rooms.quantity - COUNT (booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
    
        booked_rooms = select(Bookings).where(
            and_(
                Bookings.room_id == room_id,
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to 

                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from 

                    ),


                )
            )
        ).cte('booked_rooms')

        """
        SELECT rooms.quantity - COUNT (booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        get_rooms_left = (
                    select(
                        (Rooms.quantity - func.count(booked_rooms.c.room_id).filter(booked_rooms.c.room_id.is_not(None))).label(
                            "rooms_left"
                        )
                    )
                    .select_from(Rooms)
                    .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )

                # Рекомендую выводить SQL запрос в консоль для сверки
                # logger.debug(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

        rooms_left = await session.execute(get_rooms_left)
        rooms_left: int = rooms_left.scalar()
        return rooms_left
    
    @classmethod
    async def add(
        cls,
        user_id:int,
        room_id: int,
        date_from: date,
        date_to: date
        ):
        async with async_session_maker() as session:
            rooms_left =  await cls.get_rooms_left(session, room_id, date_from, date_to)
       
            if rooms_left != None: 
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Bookings).values(
                    room_id = room_id,
                    user_id= user_id,
                    date_from = date_from,
                    date_to = date_to, 
                    price = price
                ).returning(Bookings)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None
            
    @classmethod
    async def find_all(cls,
                       user_id
                       ):
        """
        select room_id, user_id, date_from, date_to, b.price, total_cost, r.image_id, r.name, r.description, r.services
        from bookings b 
        left join rooms r on b.room_id = r.id
        where b.user_id = 3; 
        """
        async with async_session_maker() as session:
            stmt = select(
                Bookings.room_id, 
                Bookings.user_id,
                Bookings.date_from,
                Bookings.date_to,
                Bookings.price,
                Bookings.total_cost,
                Bookings.total_days,
                Rooms.image_id,
                Rooms.name,
                Rooms.description,
                Rooms.services
            ).select_from(Bookings).join(Rooms, Bookings.room_id == Rooms.id, isouter=True).filter(Bookings.user_id == user_id)
        result = await session.execute(stmt)
        return result.mappings().all()
    

    @classmethod
    async def delete_booking(cls, 
                             booking_id,
                             user_id
                             ):
        async with async_session_maker() as session:
            stmt = delete(Bookings).where((Bookings.id == booking_id) & (Bookings.user_id == user_id))
        await session.execute(stmt)
        await session.commit()
    