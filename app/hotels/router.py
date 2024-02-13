from datetime import date
from typing import Annotated
from fastapi import APIRouter, Path, Query
from app.hotels.dao import HotelsDAO
from app.hotels.shemas import SHotelInfo


router = APIRouter(
    prefix='/hotels',
    tags=['Hotels']
)

@router.get('/{location}')
async def get_hotels(location: Annotated[str, Path()],
                     date_from: Annotated[date, Query()],
                     date_to: Annotated[date, Query()]) -> list[SHotelInfo]:
    
    return await HotelsDAO.get_hotels_with_free_rooms(location=location,date_from=date_from,date_to=date_to)