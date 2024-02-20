from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from app.bookings.router import router as bookings_router
from app.users.router import router as users_router
from app.hotels.router import router as hotels_router
from app.hotels.rooms.router import router as rooms_router
from app.pages.router import router as pages_router
from fastapi.staticfiles import StaticFiles
from app.images.router import router as img_router
from redis import asyncio as aioredis
from fastapi_cache.backends.redis import RedisBackend
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # при запуске
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

app = FastAPI(lifespan=lifespan)

app.mount(path='/static', app=StaticFiles(directory='app/static'), name='static')

app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(pages_router)
app.include_router(img_router)




# app = VersionedFastAPI(app,
#     version_format='{major}',
#     prefix_format='/api/v{major}',
#     lifespan=lifespan,
# )