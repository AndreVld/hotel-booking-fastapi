from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Path, Query
from fastapi_cache.decorator import cache

from app.exceptions import (
    CannotBookHotelForLongPeriod,
    DateFromCannotBeAfterDateTo,
    DateFromCannotBeEqualDate,
    ServerErrorException,
)
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotelInfo, SHotels

router = APIRouter(prefix="/hotels", tags=["Hotels / Rooms"])


@router.get("/{location}")
async def get_hotels_by_location_and_date(
    location: str,
    date_from: Annotated[date, Query(description=f"example: {datetime.now().date()}")],
    date_to: Annotated[
        date,
        Query(description=f"example: {datetime.now().date() + timedelta(days=25)}"),
    ],
) -> list[SHotelInfo]:

    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if date_from == date_to:
        raise DateFromCannotBeEqualDate
    if (date_to - date_from).days > 31:
        raise CannotBookHotelForLongPeriod

    hotels = await HotelsDAO.get_hotels_by_location(
        location=location, date_from=date_from, date_to=date_to
    )
    if hotels is None:
        raise ServerErrorException

    return hotels


@router.get("/id/{hotel_id}")
@cache(expire=60)
async def get_hotel_by_id(hotel_id: Annotated[int, Path()]) -> SHotels:
    return await HotelsDAO.find_by_id(hotel_id)
