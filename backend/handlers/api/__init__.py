__all__ = ["router"]
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from backend.handlers.api import v1

router = APIRouter(
    prefix="/api",
    # tags=["/api/"],


    # tags=["API"],
    # default_response_class=JSONResponse
)

router.include_router(v1.router)
