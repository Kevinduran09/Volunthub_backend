from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy.orm import DeclarativeBase
from settings import settings
DATABASE_URL = f"postgressql://{settings.DB_USER}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass
