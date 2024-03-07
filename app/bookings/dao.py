from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import and_, delete, exists, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session
from app.hotels.rooms.models import Rooms
from app.logger import logger


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def find_all(cls, user_id) -> list[dict | None] | None:
        async with async_session() as session:
            try:
                bookings = await session.execute(
                    select(
                        cls.model.__table__.columns,
                        Rooms.description,
                        Rooms.image_id,
                        Rooms.services,
                        Rooms.name,
                    )
                    .select_from(cls.model)
                    .join(Rooms, Rooms.id == cls.model.room_id, isouter=True)
                    .where(cls.model.user_id == user_id)
                )
                result = bookings.mappings().all()
                logger.info(f"Found {len(result)} bookings for user_id:{user_id}.")
                return result
            except (SQLAlchemyError, Exception) as ex:
                extra = {
                    "param": {
                        "user_id": user_id,
                    }
                }
                logger.error(
                    "Exception: Cannot find all booking", extra=extra, exc_info=True
                )
                return None

    @classmethod
    async def get_num_of_available_rooms(
        cls,
        room_id: int,
        date_from: date,
        date_to: date,
    ) -> int:
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
            booked_rooms = (
                select(cls.model)
                .where(
                    and_(
                        cls.model.room_id == room_id,
                        or_(
                            and_(
                                cls.model.date_from >= date_from,
                                cls.model.date_from <= date_to,
                            ),
                            and_(
                                cls.model.date_from <= date_from,
                                cls.model.date_to > date_from,
                            ),
                        ),
                    )
                )
                .cte("booked_rooms")
            )

            get_rooms_left = (
                select(
                    (
                        Rooms.quantity
                        - func.count(booked_rooms.c.room_id).filter(
                            booked_rooms.c.room_id.is_not(None)
                        )
                    ).label("rooms_left")
                )
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )

            # print(
            #     get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True})
            # )

            rooms_left = await session.execute(get_rooms_left)
            rooms_left = rooms_left.scalar()
            return rooms_left

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        try:
            rooms_left = await cls.get_num_of_available_rooms(
                room_id=room_id, date_from=date_from, date_to=date_to
            )

            if not rooms_left:
                return None

            async with async_session() as session:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = (
                    insert(cls.model)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(cls.model)
                )
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()

        except (SQLAlchemyError, Exception) as ex:
            if isinstance(ex, SQLAlchemyError):
                msg = "Database"
            elif isinstance(ex, Exception):
                msg = "Unknown"

            msg += " Exc : Cannot add booking"
            extra = {
                "param": {
                    "room_id": room_id,
                    "user_id": user_id,
                    "date_from": date_from,
                    "date_to": date_to,
                }
            }
            logger.error(msg, extra=extra, exc_info=True)

            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    async def delete(cls, booking_id, user_id: int) -> None:
        extra = {"param": {"booking_id": booking_id, "user_id": user_id}}
        try:
            async with async_session() as session:
                booking = await session.execute(
                    select(
                        exists().where(
                            and_(
                                cls.model.id == booking_id, cls.model.user_id == user_id
                            )
                        )
                    )
                )
                if booking.scalar():
                    await session.execute(
                        delete(cls.model).where(
                            and_(
                                cls.model.id == booking_id, cls.model.user_id == user_id
                            )
                        )
                    )
                    await session.commit()
                    logger.info("Booking successfully deleted.", extra=extra)
                else:
                    logger.warning("Booking not found for deletion.", extra=extra)
        except SQLAlchemyError as ex:
            logger.error("Database Exc: Can't delete booking", exc_info=True)
            return "Exp"
