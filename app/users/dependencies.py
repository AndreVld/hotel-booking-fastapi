from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    UserIsNotPresentException,
)
from app.users.dao import UsersDAO


def get_token(request: Request):
    if token := request.cookies.get("access_token"):
        return token
    raise TokenAbsentException


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload: dict = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrectTokenFormatException

    """Key 'exp' is automatically checked by jwt.decode()"""
    # expire: str = payload.get('exp')
    # if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
    #     raise TokenExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_by_id(model_id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user
