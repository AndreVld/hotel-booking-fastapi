from datetime import datetime
from pydantic import BaseModel


class SBookings(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: datetime
    date_to: datetime
    price: int
    total_days: int
    total_cost: int

    class Config:
        from_attributes = True
    
class SBookingsWithRooms(SBookings):
    name: str
    description: str
    image_id: int
    services: list[str]
    