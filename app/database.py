from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import NullPool


if settings.MODE == 'TEST':
    DATABASE_URL = f'postgresql+asyncpg://{settings.TEST_DB_USER}:{settings.TEST_DB_PASS}@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}'
    DATABASE_PARAMS = {'poolclass': NullPool}
else:
    DATABASE_URL = f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
    DATABASE_PARAMS = {}


engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session = async_sessionmaker(engine, expire_on_commit=False)

engine_nullpool = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_nullpool = async_sessionmaker(engine_nullpool, expire_on_commit=False)



class Base(DeclarativeBase):
    pass
