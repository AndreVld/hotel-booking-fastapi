from app.dao.base import BaseDAO
from app.bookings.models import Bookings


class BokingDAO(BaseDAO):
    model = Bookings
