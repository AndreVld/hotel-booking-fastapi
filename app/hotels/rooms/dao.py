from datetime import date
from sqlalchemy import and_, func, or_, select
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms
from app.database import async_session


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all(cls, hotel_id: int, date_from: date, date_to: date):
        booked_rooms = select(Bookings).where(
            or_(
                and_(Bookings.date_from >= date_from,
                     Bookings.date_from <= date_to
                    ),
                and_(Bookings.date_from >= date_from,
                     Bookings.date_to > date_to
                    ),
            )
        ).cte('booked_rooms')

        days_book_room = (date_to - date_from).days

        async with async_session() as session:
            rooms = await session.execute(
                select(
                    cls.model.__table__.columns,
                    (cls.model.price * days_book_room).label('total_cost'),
                    (cls.model.quantity - func.count(booked_rooms.c.id)).label('rooms_left')
                ).select_from(cls.model).join(
                    booked_rooms, booked_rooms.c.room_id == cls.model.id, isouter=True
                ).where(
                    cls.model.hotel_id == hotel_id
                ).group_by(cls.model.id)
            )

            return rooms.mappings().all()