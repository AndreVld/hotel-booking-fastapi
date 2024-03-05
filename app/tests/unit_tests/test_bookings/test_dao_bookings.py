import pytest
from app.bookings.dao import BookingDAO
from datetime import datetime as dt


@pytest.mark.parametrize('user_id', [1, 2, 12])
async def test_find_all(user_id):
    booking = await BookingDAO.find_all(user_id=user_id)
    expected_keys = {
        'id', 
        'room_id', 
        'user_id', 
        'date_from', 
        'date_to', 
        'price', 
        'total_cost', 
        'total_days', 
        'description', 
        'image_id', 
        'services', 
        'name'
    }
    
    assert isinstance(booking, list)
    for item in booking:
        assert set(item.keys()) == expected_keys

@pytest.mark.parametrize('room_id, date_from, date_to, free_rooms',[
    (1, dt.strptime('2023-06-05', '%Y-%m-%d'),dt.strptime('2023-06-25', '%Y-%m-%d'), 5),
    (2, dt.strptime('2023-04-01', '%Y-%m-%d'),dt.strptime('2023-04-19', '%Y-%m-%d'), 10),
    (3, dt.strptime('2023-03-10', '%Y-%m-%d'),dt.strptime('2023-03-24', '%Y-%m-%d'), 15),
    (4, dt.strptime('2023-03-10', '%Y-%m-%d'),dt.strptime('2023-03-24', '%Y-%m-%d'), 8),
])
async def test_get_num_of_available_rooms(room_id, date_from, date_to, free_rooms):
    num_free_rooms = await BookingDAO.get_num_of_available_rooms(
        room_id, 
        date_from, 
        date_to
    )
    assert num_free_rooms == free_rooms

@pytest.mark.parametrize('user_id, room_id, date_from, date_to, no_rooms_available',[
    (1, 6, dt.strptime('2026-03-10', '%Y-%m-%d'),dt.strptime('2026-03-24', '%Y-%m-%d'), False),
    *[(2, 1, dt.strptime('2026-07-10', '%Y-%m-%d'), dt.strptime('2026-07-24', '%Y-%m-%d'), False) for _ in range(5)],
    (2, 1, dt.strptime('2026-07-10', '%Y-%m-%d'), dt.strptime('2026-07-24', '%Y-%m-%d'), True)
])
async def test_add_booking(user_id, room_id, date_from, date_to, no_rooms_available):
    booking = await BookingDAO.add(user_id, room_id, date_from, date_to)

    if no_rooms_available:
        assert booking is None
    else:
        assert booking
        assert booking.user_id == user_id
        assert booking.room_id == room_id
