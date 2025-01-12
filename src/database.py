__all__ = ["DBSession"]
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .settings import async_session_maker


async def create_database_session():
    session = async_session_maker()
    try:
        yield session
    finally:
        await session.aclose()


DBSession = Annotated[AsyncSession, Depends(dependency=create_database_session)]
