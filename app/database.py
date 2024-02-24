from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import NullPool


DATABASE_URL = f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'


engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

engine_nullpool = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_nullpool = async_sessionmaker(engine_nullpool, expire_on_commit=False)



class Base(DeclarativeBase):
    pass
