from fastapi import APIRouter, Depends, Request
from app.bookings.dao import BokingDAO
from app.bookings.schemas import SBookings
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования']
)

@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)): #-> list[SBookings]:
    print(user, type(user), user.email)
    return await BokingDAO.find_all(user_id=user.id)
