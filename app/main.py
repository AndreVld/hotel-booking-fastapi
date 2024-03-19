from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator
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
from app.importer.router import router as import_file_router
from app.users.router import auth_router, users_router


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

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(img_router)
app.include_router(import_file_router)


app = VersionedFastAPI(
    app, version_format="{major}", prefix_format="/v{major}", lifespan=lifespan
)

admin = Admin(app, engine, authentication_backend=auth_backend)

admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     logger.debug(
#         "Request handling time", extra={"process_time": round(process_time, 4)}
#     )
#     return response
