import calendar
import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models import ScheduleTemplate, User
from app.repositories.schedule_template_repositories import ScheduleTemplateRepositories
from app.repositories.shift_limit_repository import ShiftLimitRepository, SpecificShiftDayRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_shift_repository import UserShiftRepository
from app.services.user_shift_service import UserShiftService
from src.enums import ShiftType
from src.exceptions import DuplicateEntryError


class AutoGenerateShiftService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session=session)
        self.user_shift_repo = UserShiftRepository(session=session)
        # self.user_shift_serv = UserShiftService(session=session)
        self.shift_repo = ShiftLimitRepository(session=session)
        self.day_repo = SpecificShiftDayRepository(session=session)
        self.session = session

    async def _get_user(self, pk: int):
        return await self.user_repo.get(pk=pk)

    async def _get_template(self, pk: int):
        return await ScheduleTemplateRepositories(session=self.session).get(pk=pk)

    async def _get_limit(self, year: int, month: int):
        month_limit = await self.shift_repo.get_month_limit(year, month)
        days_limit = await self.day_repo.get_all_specific_days_for_month(year, month)
        return {
            "month": month_limit,
            "days_limit": days_limit,
        }

    async def autogenerate(self, user_id: int, year: int, month: int):
        user: User = await self._get_user(pk=user_id)   # noqa
        if not user.start_date or not user.shift_template_id:
            raise HTTPException(status_code=400, detail="Нет необходимых атрибутов: либо графика,"
                                                        " либо даты с которой начал работать по графику.")
        template: ScheduleTemplate = await self._get_template(pk=user.shift_template_id) # noqa
        work_days, rest_days = template.work_days, template.rest_days
        cycle = work_days + rest_days
        start_date = user.start_date
        cycle_count = 0
        if start_date.month != month:
            div_timedelta = datetime.date(year, month, 1) - start_date
            start_date += datetime.timedelta(days=(div_timedelta.days // cycle) * cycle)
            if tmp := div_timedelta.days % cycle:
                cycle_count += tmp
                start_date += datetime.timedelta(days=tmp)
        _, last_day_of_month = calendar.monthrange(year, month)
        work_list = list(range(work_days))
        for i in range(start_date.day, last_day_of_month + 1):
            if cycle_count % cycle in work_list:
                try:
                    await self.user_shift_repo.save(
                        form={
                            "user_id": user_id,
                            "date": datetime.date(year=year, month=month, day=i),
                            "shift_template_id": template.id,
                            "shift_type": ShiftType.SCHEDULE,
                        }
                    )
                except DuplicateEntryError:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail=f"Возникла ошибка при генерации смены {year}-{month}-{i} для {user_id=}")
            cycle_count += 1
        return "OK"
