__all__ = ["router"]
from fastapi import APIRouter

from backend.handlers.api.v1 import users
from backend.handlers.api.v1 import users_shifts
from backend.handlers.api.v1 import shifts
from backend.handlers.api.v1 import shift_liimit
from backend.handlers.api.v1 import shedule_template

router = APIRouter(
    prefix="/v1",
    # tags=["V1"]
)

router.include_router(users.router)
router.include_router(users_shifts.router)
router.include_router(shift_liimit.router)
router.include_router(shedule_template.router)
router.include_router(shifts.router)

