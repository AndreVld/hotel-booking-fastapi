from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings as st

DATABASE_URL = "postgresql+asyncpg://"
if st.MODE == "TEST":
    DATABASE_URL += f"{st.TEST_DB_USER}:{st.TEST_DB_PASS}@{st.TEST_DB_HOST}:{st.TEST_DB_PORT}/{st.TEST_DB_NAME}"
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL += f"{st.DB_USER}:{st.DB_PASS}@{st.DB_HOST}:{st.DB_PORT}/{st.DB_NAME}"
    DATABASE_PARAMS = {}


engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session = async_sessionmaker(engine, expire_on_commit=False)

engine_nullpool = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_nullpool = async_sessionmaker(engine_nullpool, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
