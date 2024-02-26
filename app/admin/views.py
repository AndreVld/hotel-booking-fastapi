from sqladmin import ModelView
from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms

from app.users.models import Users


class UserAdmin(ModelView, model=Users):
    # column_list = '__all__'
    column_exclude_list = [Users.hashed_password]
    column_searchable_list = [Users.email, Users.id]
    column_sortable_list = [Users.email, Users.id]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = 'User'
    name_plural = 'Users'
    icon = "fa-solid fa-user"
    

class BookingsAdmin(ModelView, model=Bookings):
    column_exclude_list = [Bookings.user_id]
    column_details_exclude_list = [Bookings.user_id, Bookings.room_id]
    name = 'Booking'
    name_plural = 'Bookings'
    icon = "fa-solid fa-book"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = '__all__'
    name = 'Hotel'
    name_plural = 'Hotels'
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    column_exclude_list = [Rooms.hotel_id]
    name = 'Room'
    name_plural = 'Rooms'
    icon = "fa-solid fa-bed"