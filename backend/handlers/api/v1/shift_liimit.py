import datetime
from typing import Literal

from fastapi import APIRouter, Path, HTTPException, Query
from starlette import status

from app.schemas.shift_limit import ShiftLimitDetail, ShiftLimitCreateForm
from app.schemas.specific_shift_day import SpecificShiftDayCreateForm, SpecificShiftDayDetail
from app.services.shift_limit_service import ShiftLimitService
from src.database import DBSession

router = APIRouter(
    prefix="/restrictions",
    tags=["Limit Shifts"]
)


@router.get(path="/{year}/{month}")
async def get_month_limit(
        session: DBSession,
        year: int = Path(ge=2000),
        month: int = Path(ge=1, le=12)
):
    max_employees = await ShiftLimitService(session=session).get(year, month)
    return max_employees


@router.get(path="/{year}/{month}/{day}",
            # response_model=ShiftLimitDetail
            )
async def get_limits_by_date(
        session: DBSession,
        year: int = Path(ge=2000),
        month: int = Path(ge=1, le=12),
        day: int = Path(ge=1, le=31)
):
    try:
        date = datetime.date(year, month, day)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="incorrect date!")
    max_employees = await ShiftLimitService(session=session).get_max_employee(date=date)
    return max_employees


@router.post(path="", response_model=ShiftLimitDetail)
async def create_limit(
        session: DBSession,
        form: ShiftLimitCreateForm
):
    obj = await ShiftLimitService(session=session).save(form=form)
    return obj


@router.post(path="/specific",
             response_model=SpecificShiftDayDetail)
async def save_specific_day_limits(
        session: DBSession,
        form: SpecificShiftDayCreateForm
):
    obj = await ShiftLimitService(session=session).save_specific_day(form=form)
    return obj


@router.get(path="/specific",
            response_model=list[SpecificShiftDayDetail])
async def get_all_specific_days_for_month(
        session: DBSession,
        year: int = Query(ge=2000),
        month: int = Query(ge=1, le=12)
):
    obj = await ShiftLimitService(session=session).get_all_specific_days(year=year, month=month)
    return obj
