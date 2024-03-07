from datetime import date
from typing import Annotated

from fastapi import Path, Query

from app.exceptions import DateFromCannotBeAfterDateTo, ServerErrorException
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRooms
from app.hotels.router import router


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: Annotated[int, Path()],
    date_from: Annotated[date, Query()],
    date_to: Annotated[date, Query()],
) -> list[SRooms]:

    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo

    rooms = await RoomsDAO.find_all(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )
    if rooms is None:
        raise ServerErrorException
    return rooms
