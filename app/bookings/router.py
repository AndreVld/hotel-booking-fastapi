from datetime import date
from typing import Annotated
from fastapi import APIRouter, Depends, Path, Request, status
from app.bookings.dao import BokingDAO
from app.bookings.schemas import SBookingsWithRooms
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix='/bookings',
    tags=['Bookings']
)

@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookingsWithRooms]:
    return await BokingDAO.find_all(user_id=user.id)

@router.post('')
async def add_booking(
    room_id: int, date_from: date, date_to: date, 
    user: Users = Depends(get_current_user),
):
    booking =  await BokingDAO.add(user_id=user.id, room_id=room_id, date_from=date_from, date_to=date_to)
    if not booking:
        raise RoomCannotBeBooked

@router.delete('/{booking_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
        booking_id: Annotated[int, Path()],
        user: Annotated[Users, Depends(get_current_user)]
        ):
    return await BokingDAO.delete(booking_id=booking_id, user_id=user.id)