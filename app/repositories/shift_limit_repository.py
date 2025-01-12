from sqlalchemy import select, extract
from sqlalchemy.orm import Mapper

from app.models.shift_limit import ShiftLimit, SpecificShiftDay
from app.repositories.alchemy_repository import SQLAlchemyRepository
from src.exceptions import LimitsNotFound


class ShiftLimitRepository(SQLAlchemyRepository):
    model = ShiftLimit

    async def get_month_limit(self, year: int, month: int) -> Mapper:
        stmt = select(self.model).filter_by(year=year, month=month)
        res = await self._run_query(statement=stmt)
        shift = res.unique().scalar_one_or_none()
        if not shift:
            raise LimitsNotFound
        return shift


class SpecificShiftDayRepository(SQLAlchemyRepository):
    model = SpecificShiftDay

    async def get_all_specific_days_for_month(self, year: int, month: int) -> list[Mapper]:
        stmt = select(self.model).filter(
            extract("year", self.model.date) == year,   # noqa
            extract("month", self.model.date) == month  # noqa
        )
        res = await self._run_query(statement=stmt)
        days = res.unique().scalars().all()
        if not days:
            raise LimitsNotFound
        return days
