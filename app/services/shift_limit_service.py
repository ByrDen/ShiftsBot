import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.repositories.abstract import AbstractRepository
from app.repositories.shift_limit_repository import ShiftLimitRepository, SpecificShiftDayRepository
from app.schemas.shift_limit import ShiftLimitCreateForm, ShiftLimitDetail, ShiftLimitEditForm
from app.schemas.specific_shift_day import SpecificShiftDayCreateForm, SpecificShiftDayDetail, SpecificShiftDayEditForm
from src.exceptions import DuplicateEntryError, LimitsNotFound


class ShiftLimitService(AbstractRepository):
    create_schema = ShiftLimitCreateForm
    edit_schema = ShiftLimitEditForm
    detail_schema = ShiftLimitDetail
    create_date_schema = SpecificShiftDayCreateForm
    edit_date_schema = SpecificShiftDayEditForm
    detail_date_schema = SpecificShiftDayDetail

    def __init__(self, session: AsyncSession):
        self.session = session
        self.shift_limit_repo = ShiftLimitRepository(session=session)
        self.specific_day_repo = SpecificShiftDayRepository(session=session)

    async def get(self, year: int, month: int):
        try:
            results = await self.shift_limit_repo.get_month_limit(year=year, month=month)
        except LimitsNotFound:
            raise HTTPException(status_code=404)
        return self.detail_schema.model_validate(obj=results)

    async def update(self, *args, **kwargs):
        raise NotImplementedError

    async def save(self, form: create_schema):
        try:
            obj = await self.shift_limit_repo.save(form=form.model_dump())
        except DuplicateEntryError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return self.detail_schema.model_validate(obj=obj)

    async def save_specific_day(self, form: create_date_schema):
        try:
            obj = await self.specific_day_repo.save(form=form.model_dump())
        except DuplicateEntryError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return self.detail_date_schema.model_validate(obj=obj)

    async def delete(self, *args, **kwargs):
        raise NotImplementedError

    async def list(self, *args, **kwargs):
        raise NotImplementedError

    async def get_max_employee(self, date: datetime.date) -> int:
        specific_day = await self.specific_day_repo.get_by_field(field_name="date", value=date)
        if len(specific_day):
            return specific_day[0].max_employees    # noqa

        year, month = date.year, date.month
        shift_limit = await self.shift_limit_repo.get_month_limit(year=year, month=month)
        if shift_limit:
            return shift_limit.max_employees    # noqa

        raise ValueError("No limit found for the given date")

    async def get_all_specific_days(self, year: int, month: int) -> list:
        try:
            specific_days = await self.specific_day_repo.get_all_specific_days_for_month(year=year, month=month)
            return [self.detail_date_schema.model_validate(obj=day) for day in specific_days]
        except LimitsNotFound:
            raise HTTPException(status_code=404)
