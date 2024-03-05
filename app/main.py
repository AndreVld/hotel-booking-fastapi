from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import auth_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UserAdmin
from app.bookings.router import router as bookings_router
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router as rooms_router
from app.hotels.router import router as hotels_router
from app.images.router import router as img_router
from app.pages.router import router as pages_router
from app.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=lifespan)

admin = Admin(app, engine, authentication_backend=auth_backend)

admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


app.mount(path="/static", app=StaticFiles(directory="app/static"), name="static")

app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(pages_router)
app.include_router(img_router)
