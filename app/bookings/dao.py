from datetime import date
from sqlalchemy import and_, func, insert, or_, select
from app.dao.base import BaseDAO
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.database import async_session, engine, AsyncSession


class BokingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int,room_id: int, date_from: date, date_to: date,):
        """
            WITH booking_rooms AS (SELECT * FROM bookings WHERE room_id=1 
            AND (date_from >= '2023-05-15' AND date_from <= '2023-06-20') 
            OR (date_from <= '2023-05-15' AND date_to > '2023-05-15'))
            SELECT rooms.quantity - COUNT(booking_rooms.room_id) FROM rooms
            LEFT JOIN booking_rooms ON booking_rooms.room_id = rooms.id
            WHERE rooms.id = 1 
            GROUP BY rooms.quantity, booking_rooms.id;
        """
        async with async_session() as session:
            booked_rooms = select(Bookings).where(
                and_(Bookings.room_id == room_id,
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
            
            get_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label('rooms_left')
                ).select_from(Rooms).join(
                    booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
                ).where(
                    Rooms.id == room_id
                ).group_by(Rooms.quantity, booked_rooms.c.room_id)

            # print(get_rooms_left.compile(engine, compile_kwargs={'literal_binds': True}))

            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()
            print(rooms_left)
            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(Bookings)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None