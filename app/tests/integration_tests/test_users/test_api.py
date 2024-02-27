from httpx import AsyncClient
import pytest


@pytest.mark.parametrize('email, password, status_code',[
    ('test@testing.com','pytest', 200),
    ('test@testing.com','pytest123', 409),
    ('test@testing2123.com','string', 200),
    ('not_email','password', 422),
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post('/auth/register', json={
        'email': email,
        'password': password,
    })

    assert response.status_code == status_code


@pytest.mark.parametrize('email, password, status_code', [
    ('test@test.com', 'tests', 200),
    ('test@test.com', 'wrongpassword', 401),
    ('user@example.com', 'string', 200),
    ('wrongemail@example.com', 'string', 401),
    
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post('/auth/login', json={
        'email': email,
        'password': password,
    })
    assert response.status_code == status_code
