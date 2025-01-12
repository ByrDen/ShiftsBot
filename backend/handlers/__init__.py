__all__ = ["router"]
from fastapi import APIRouter

from backend.handlers import api

router = APIRouter()

router.include_router(api.router)
