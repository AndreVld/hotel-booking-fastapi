from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from app.config import settings


from app.users.auth import authenticate_user, create_access_token
from app.users.dependencies import get_current_user


class AdminAuth(AuthenticationBackend):

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        if  user:= await authenticate_user(email, password):

            access_token = create_access_token({'sub': str(user.id)})
            request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:

        if token:= request.session.get("token"):
            if user:= await get_current_user(token):
                return True



        return RedirectResponse(request.url_for('admin:login'), status_code=302)


auth_backend = AdminAuth(secret_key=settings.SECRET_KEY)
