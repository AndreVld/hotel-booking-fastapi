from datetime import date
from fastapi import APIRouter, Depends, Request
from app.bookings.dao import BokingDAO
from app.bookings.schemas import SBookings
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования']
)

@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookings]:
    return await BokingDAO.find_all(user_id=user.id)

@router.post('')
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_current_user),
):
    booking =  await BokingDAO.add(user_id=user.id, room_id=room_id, date_from=date_from, date_to=date_to)
    if not booking:
        raise RoomCannotBeBooked



