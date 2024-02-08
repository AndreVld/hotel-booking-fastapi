from fastapi import APIRouter
from app.bookings.dao import BokingDAO
from app.bookings.shemas import SBookings


router = APIRouter(
    prefix='/bookings',
    tags=['Бронирование']
)

@router.get('')
async def get_bookings() -> list[SBookings]:
    return await BokingDAO.find_all()
