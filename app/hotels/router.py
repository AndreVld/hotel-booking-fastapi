from datetime import date, datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Path, Query
from app.exceptions import DateFromCannotBeAfterDateTo
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotelInfo, SHotels
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix='/hotels',
    tags=['Hotels / Rooms']
)

@router.get('/{location}')
@cache(expire=20)
async def get_hotels_by_location_and_date(
        location: str,
        date_from: Annotated[date, Query(example=datetime.now().date())],
        date_to: Annotated[date, Query(example=datetime.now().date() + timedelta(days=25))]
    ) -> list[SHotelInfo]:
    
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo

    hotels = await HotelsDAO.get_hotels_by_location(
        location=location,
        date_from=date_from,
        date_to=date_to
    )
    return hotels

@router.get('/id/{hotel_id}')
@cache(expire=60)
async def get_hotel_by_id(hotel_id: Annotated[int, Path()]) -> SHotels:
    return await HotelsDAO.find_by_id(hotel_id)