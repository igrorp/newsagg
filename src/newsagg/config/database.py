import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from newsagg.schemas.article import Base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


# Dependency
async def get_session():
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
