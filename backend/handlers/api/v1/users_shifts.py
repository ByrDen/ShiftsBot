import datetime

from fastapi import APIRouter, Path, Query, Depends, HTTPException
from starlette import status

from app.schemas.users_shifts import UserShiftDetail, UserShiftCreateForm
from app.services.user_shift_service import UserShiftService
from backend.dependency import validate_user
from src.database import DBSession

router = APIRouter(
    prefix="/users/{user_id}/shifts",
    tags=["Users Shifts"],
)


@router.get(path="", response_model=list[UserShiftDetail])
async def get_user_shifts_for_current_month(
    session: DBSession,
    user_id: int = Path(ge=1),
    year: int = Query(default=None, ge=2000),
    month: int = Query(default=None, ge=1, le=12)
):
    return await UserShiftService(session=session).get_user_shifts_for_current_month(user_id=user_id,
                                                                                     year=year,
                                                                                     month=month)


@router.post(path="", response_model=UserShiftDetail, status_code=201)
async def add_users_shift(
        session: DBSession,
        form: UserShiftCreateForm,
        user_id: int = Depends(validate_user),
):
    resp = await UserShiftService(session=session).save(user_id=user_id, form=form)
    return resp

# @router.put(path="")


@router.delete(path="")
async def delete_shift(
        session: DBSession,
        user_id: int = Depends(validate_user),
        year: int = Query(default=..., ge=2020),
        month: int = Query(default=..., ge=1, le=12),
        day: int = Query(default=..., ge=1, le=31)
):
    """ Удаление указанной смены пользователя, если день не указан,
        то будут удалены смены указанного(или текущего) месяца."""
    # today = datetime.date.today()
    # year = today.year if (not year) else year
    # month = today.month if not month else month
    date = datetime.date(year, month, day)
    await UserShiftService(session=session).delete(user_id=user_id, date=date)

    return "OK"
