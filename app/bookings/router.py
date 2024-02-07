from fastapi import APIRouter
from app.bookings.dao import BokingDAO


router = APIRouter(
    prefix='/bookings',
    tags=['Бронирование']
)


@router.get('')
async def get_bookings():
    return await BokingDAO.find_all()