import pytest

from app.users.dao import UsersDAO

@pytest.mark.parametrize('user_id, email, exists', [
    (1, 'test@test.com', True),
    (2, 'user@example.com',  True),
    (12, "doesn't exist", False)
])
async def test_find_user_by_id(user_id, email, exists):
    user = await UsersDAO.find_by_id(user_id)

    if exists:
        assert user.id == user_id
        assert user.email == email    
    else:
        assert not user


@pytest.mark.parametrize('user_id, email, exists', [
    (1, 'test@test.com', True),
    (2, 'user@example.com',  True),
    (12, "doesn't exist", False)
])
async def test_find_one_or_none(user_id, email, exists):
    user = await UsersDAO.find_one_or_none(email=email)

    if exists:
        assert user.id == user_id
        assert user.email == email    
    else:
        assert user is None
