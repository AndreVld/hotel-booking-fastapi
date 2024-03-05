from datetime import datetime as dt
import pytest
from app.bookings.dao import BookingDAO


@pytest.mark.parametrize('user_id, room_id, date_from, date_to', [
    (1, 6, dt.strptime('2026-03-10', '%Y-%m-%d'),dt.strptime('2026-03-24', '%Y-%m-%d')),
    (2, 7, dt.strptime('2026-05-10', '%Y-%m-%d'), dt.strptime('2026-05-24', '%Y-%m-%d')),
    (1, 5, dt.strptime('2026-06-10', '%Y-%m-%d'),dt.strptime('2026-06-24', '%Y-%m-%d')),
    (2, 1, dt.strptime('2026-07-10', '%Y-%m-%d'), dt.strptime('2026-07-24', '%Y-%m-%d')),
]) 
async def test_crud_bookings(user_id, room_id, date_from, date_to):
    new_booking = await BookingDAO.add(
        user_id = user_id,
        room_id = room_id,
        date_from = date_from,
        date_to = date_to,
    )
    assert new_booking.user_id == user_id
    assert new_booking.room_id == room_id

    booking = await BookingDAO.find_by_id(new_booking.id)
    assert booking.user_id == user_id
    assert booking.room_id == room_id

    await BookingDAO.delete(booking.id, booking.user_id)

    booking = await BookingDAO.find_by_id(new_booking.id)
    assert booking is None


async def test_add_and_get_booking():
    new_booking = await BookingDAO.add(
        user_id = 2,
        room_id = 2,
        date_from = dt.strptime('2026-07-10', '%Y-%m-%d'),
        date_to = dt.strptime('2026-07-24', '%Y-%m-%d'),
    )

    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    new_booking = await BookingDAO.find_by_id(new_booking.id)

    assert new_booking is not None

