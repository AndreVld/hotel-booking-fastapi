from datetime import datetime
from fastapi import Response
from httpx import AsyncClient
import pytest


@pytest.mark.parametrize('room_id, date_from, date_to, booked_rooms, status_code', [
    (4, '2030-05-01','2030-05-15', booked_rooms, 200) for booked_rooms in range(3, 11)
    ] + [
        (4, '2030-05-01','2030-05-15', 10, 409)
    ]
)
async def test_add_and_get_booking(room_id, date_from, date_to,booked_rooms, status_code, authenticated_ac: AsyncClient):
    responce: Response = await authenticated_ac.post('/bookings', params={
        'room_id' : room_id,
        'date_from': date_from,
        'date_to' : date_to,
    })

    assert responce.status_code == status_code
    responce: Response = await authenticated_ac.get('/bookings')
    assert len(responce.json()) == booked_rooms



@pytest.mark.parametrize('email, password',[
    ('test@test.com', 'tests'),
    ('user@example.com', 'string'),
])
async def test_get_and_delete_bookings(email, password, ac: AsyncClient):
    await ac.post('/auth/login', json={
            'email':email,
            'password': password,
        })
    assert ac.cookies['access_token']

    response: Response = await ac.get('/bookings')

    assert response.status_code == 200
    for booking in response.json():
        response: Response = await ac.delete(f'/bookings/{booking.get("id")}')
        assert response.status_code == 204
    
    response: Response = await ac.get('/bookings')
    
    assert response.status_code == 200
    assert len(response.json()) == 0
