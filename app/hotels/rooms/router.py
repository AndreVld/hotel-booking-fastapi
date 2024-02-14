from datetime import date
from typing import Annotated

from fastapi import Path, Query
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRooms
from app.hotels.router import router

@router.get('/{hotel_id}/rooms')
async def get_rooms(
                hotel_id: Annotated[int, Path()],
                date_from: Annotated[date, Query()],
                date_to: Annotated[date, Query()]) -> list[SRooms]:
    
    return await RoomsDAO.find_all(hotel_id=hotel_id, date_from=date_from, date_to=date_to)