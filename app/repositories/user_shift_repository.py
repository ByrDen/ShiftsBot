import datetime
from typing import Any

from sqlalchemy import select, extract

from src.exceptions import ItemNotFound
from .alchemy_repository import SQLAlchemyRepository
from ..models import User
from ..models.users_shifts import UsersShifts


class UserShiftRepository(SQLAlchemyRepository):
    model = UsersShifts

    async def get_user_shifts_by_date(self, user_id: int, year: int, month: int) -> list[UsersShifts]:
        stmt = select(self.model).join(User, User.id == UsersShifts.user_id).filter(
                UsersShifts.user_id == user_id,
                extract("year", UsersShifts.date) == year,
                extract("month", UsersShifts.date) == month
            )
        result = await self.session.scalars(stmt)
        shifts = result.unique().all()

        if not shifts:
            raise ItemNotFound(f"No shifts found for user {user_id} in {year}-{month}")

        return shifts

    async def get_shifts_with_users(self, user_id: int, date: datetime.date):
        # stmt = select(self.model).join(User, User.id == self.model.user_id, isouter=True, full=True).filter(
        #     self.model.user_id == user_id,
        #     self.model.date == date
        # )
        stmt = select(User.last_name).join(self.model, self.model.user_id == User.id).filter(
            self.model.user_id == user_id,
            self.model.date == date
        )
        print(stmt)
        result = await self.session.scalars(stmt)
        shifts = result.unique().one_or_none()
        if not shifts:
            raise ItemNotFound(f"No shifts found for user {user_id} in {date}")

        return shifts

    # async def get_list_shifts_by_date(self, date: datetime.date) -> list[UsersShifts]:
    #     stmt = select(self.model).filter(self.model.date == date)
    #     result = self._run_query(statement=stmt)
    #     shifts = result.unique().scalars().all()
    #
    #     if not shifts:
    #         raise ItemNotFound(f"No shifts found for {date}")
    #
    #     return shifts

