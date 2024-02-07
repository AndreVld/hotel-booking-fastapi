from fastapi import FastAPI, Query, Depends
from datetime import date
from pydantic import BaseModel



app = FastAPI()

class HotelsSearchArgs:
    def __init__(self,
        location: str,
        date_from: date,
        date_to: date,
        has_spa: bool = None,
        stars: int = Query(None, ge=1, le=5)
        ) -> None:
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars


class SHotel(BaseModel):
    address: str
    name: str
    stars: int
    # has_spa: bool


@app.get('/hotels')
def get_hotels(search_args: HotelsSearchArgs = Depends()) -> list[SHotel]:
    hotels = [
        {
            "address": "Nevskiy, 43, SPB",
            "name": "SPB-hotel",
            "stars": 5,
        }
    ]
    return hotels


class Sbooking(BaseModel):
    room_id: int
    date_from: date
    date_too: date


@app.post("/bookings")
def add_booking(booking: Sbooking):
    pass
