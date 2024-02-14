from datetime import date
from sqlalchemy import and_, delete, func, insert, or_, select
from app.dao.base import BaseDAO
from app.bookings.models import Bookings
from app.exceptions import NotFound
from app.hotels.rooms.models import Rooms
from app.database import async_session, engine, AsyncSession


class BokingDAO(BaseDAO):
    model = Bookings


    @classmethod
    async def find_all(cls, user_id):
        async with async_session() as session:
            bookings = await session.execute(select(
                    cls.model.__table__.columns, 
                    Rooms.description,
                    Rooms.image_id,
                    Rooms.services,
                    Rooms.name
                ).select_from(cls.model
                ).join(Rooms, Rooms.id == cls.model.room_id, isouter=True
                ).where(cls.model.user_id == user_id
                ))
            
            return bookings.mappings().all()
        
                       

    @classmethod
    async def get_num_of_available_rooms(
        cls, room_id: int, 
        date_from: date, date_to: date,) -> int:
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
            booked_rooms = select(cls.model).where(
                and_(cls.model.room_id == room_id,
                    or_(
                        and_(
                            cls.model.date_from >= date_from, 
                            cls.model.date_from <= date_to
                            ), 
                        and_(
                            cls.model.date_from <= date_from, 
                            cls.model.date_to > date_from
                            ),
                        ) 
                    )
                ).cte('booked_rooms')
            
            get_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label('rooms_left')
                ).select_from(Rooms).join(
                    booked_rooms, booked_rooms.c.room_id == Rooms.id, 
                ).where(
                    Rooms.id == room_id
                ).group_by(Rooms.quantity, booked_rooms.c.room_id)

            # print(get_rooms_left.compile(engine, compile_kwargs={'literal_binds': True}))

            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()

            return rooms_left

    @classmethod
    async def add(cls, user_id: int,room_id: int, date_from: date, date_to: date,):

        rooms_left = await cls.get_num_of_available_rooms(room_id=room_id,
                                                    date_from=date_from,
                                                    date_to=date_to)

        if rooms_left > 0:

            async with async_session() as session:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(cls.model).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(cls.model)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
        else:
            return None
    
    @classmethod
    async def delete(cls, booking_id, user_id: int):
        async with async_session() as session:
            result = await session.execute(
                        delete(cls.model)
                        .where(
                            and_(
                                cls.model.id == booking_id,
                                cls.model.user_id == user_id
                                )
                            )
                        .returning(cls.model)
                    )
            booking = result.scalar()
            if not booking:
                raise NotFound
            await session.commit()
