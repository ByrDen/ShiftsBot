import datetime

from fastapi import APIRouter, Query, Depends

from app.schemas.users_shifts import UserShiftDetail
from app.services.auto_generate_shift_service import AutoGenerateShiftService
from app.services.user_shift_service import UserShiftService
from backend.dependency import validate_user
from src.database import DBSession

router = APIRouter(
    prefix="/shifts",
    tags=["Shifts"]
)


@router.get(path="/", response_model=list[UserShiftDetail])
async def get_all_shifts_for_current_month(
    session: DBSession,
    year: int, month: int
):
    serv = UserShiftService(session=session)
    return await serv.get_list_shifts_for_current_month(year, month)


@router.get(path="", response_model=list[UserShiftDetail])
async def get_users_on_shifts(
        session: DBSession,
        year: int = Query(default=..., ge=2020),
        month: int = Query(default=..., ge=1, le=12),
        day: int = Query(default=..., ge=1, le=31)
):
    if day:
        date = datetime.date(year, month, day)
    service = UserShiftService(session=session)
    shifts = await service.list(date=date)
    return shifts


@router.get(path="/bum")
async def get_bum(
        session: DBSession,
        year: int, month: int, day: int ,
        user_id: int = Depends(validate_user),
):
    date = datetime.date(year, month, day)
    service = UserShiftService(session=session)
    shifts = await service.get(user_id=user_id, date=date)
    return shifts


@router.get(path="/autogenerate")
async def autogenerate(
        session: DBSession,
        user_id: int,
        year: int, month: int
):
    serv = AutoGenerateShiftService(session=session)
    return await serv.autogenerate(user_id=user_id, year=year, month=month)
