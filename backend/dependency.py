from fastapi import Depends, HTTPException

from app.repositories.user_repository import UserRepository
from src.database import DBSession
from src.exceptions import ItemNotFound


async def validate_user(user_id: int, session: DBSession):
    try:
        await UserRepository(session=session).get(pk=user_id)
        return user_id
    except ItemNotFound:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
