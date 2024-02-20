from datetime import date
from operator import and_
from sqlalchemy import func, or_, select
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.database import async_session
from app.hotels.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_hotels_by_location(
        cls, 
        location: str, 
        date_from: date, 
        date_to: date,
    ):
        booked_rooms = select(
            Bookings.room_id, func.count(Bookings.room_id).label('rooms_booked')
            ).select_from(Bookings).where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from)
                )
            ).group_by(Bookings.room_id).cte('booked_rooms')
        
        rooms =  select(
            Rooms.hotel_id,
            func.sum(Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)).label('rooms_left')
            ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).group_by(Rooms.hotel_id).cte('rooms')
        
        async with async_session() as session:
            hotels = await session.execute(
                select(
                    cls.model.__table__.columns,
                    rooms.c.rooms_left
                    ).select_from(cls.model).join(
                        rooms, rooms.c.hotel_id == cls.model.id, isouter=True
                    ).where(
                            and_(
                                cls.model.location.like(f'%{location}%'),
                                rooms.c.rooms_left > 0
                                )
                            )
                )
            
            return hotels.mappings().all()
