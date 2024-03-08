from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from fastapi_versioning import version

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookings
from app.config import settings
from app.exceptions import (
    DateFromCannotBeAfterDateTo,
    RoomCannotBeBooked,
    ServerErrorException,
)
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
@version(1)
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookings]:
    bookings = await BookingDAO.find_all(user_id=user.id)
    if bookings is None:
        raise ServerErrorException
    return bookings


@router.post("")
@version(1)
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):

    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo

    booking = await BookingDAO.add(
        user_id=user.id, room_id=room_id, date_from=date_from, date_to=date_to
    )
    if booking is None:
        raise RoomCannotBeBooked

    if settings.MODE != "TEST":
        booking_dict = SBookings.model_validate(booking).model_dump()
        send_booking_confirmation_email.delay(booking_dict, user.email)

    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
@version(1)
async def delete_booking(
    booking_id: Annotated[int, Path()],
    user: Annotated[Users, Depends(get_current_user)],
):
    if await BookingDAO.delete(booking_id=booking_id, user_id=user.id) == "Exp":
        raise ServerErrorException
