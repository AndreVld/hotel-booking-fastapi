from fastapi import APIRouter, Depends, Response
from fastapi_versioning import version

from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
users_router = APIRouter(prefix="/users", tags=["Users"])


@auth_router.post("/register")
@version(1)
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@auth_router.post("/login")
@version(1)
async def login_user(responce: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    responce.set_cookie("access_token", access_token, httponly=True)
    return user


@auth_router.post("/logout")
@version(1)
async def logout_user(responce: Response):
    responce.delete_cookie("access_token")


@users_router.get("/me")
@version(1)
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
