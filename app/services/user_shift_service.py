import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.repositories.abstract import AbstractRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_shift_repository import UserShiftRepository
from app.schemas.users_shifts import UserShiftCreateForm, UserShiftEditForm, UserShiftDetail
from src.exceptions import ItemNotFound, DuplicateEntryError


class UserShiftService(AbstractRepository):
    create_schema = UserShiftCreateForm
    edit_schema = UserShiftEditForm
    detail_schema = UserShiftDetail

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = UserShiftRepository(session=session)
        self.user_repo = UserRepository(session=session)

    async def get(self, user_id: int, date: datetime.date):
        obj = await self.repository.get_shifts_with_users(user_id=user_id, date=date)
        print(obj)
        return self.detail_schema.model_validate(obj=obj)

    async def update(self, *args, **kwargs):
        pass

    async def save(self, user_id: int, form: create_schema):
        try:
            data = {**form.model_dump() | {"user_id": user_id}}
            obj = await self.repository.save(form=data)
        except DuplicateEntryError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This Shift was add early")
        return self.detail_schema.model_validate(obj=obj)

    async def delete(self, user_id: int, date: datetime.date):
        try:
            await self.repository.delete_by_date(date=date)
        except Exception:
            raise HTTPException(status_code=422)

    async def list(
            self,
            order_by: str = None,
            order: str = None,
            limit: int = None,
            offset: int = None,
            **kwargs) -> list[detail_schema]:
        shifts = await self.repository.list(order_by=order_by, order=order, limit=limit, offset=offset, **kwargs)
        return [self.detail_schema.model_validate(obj=obj) for obj in shifts]

    async def get_pk_by_date(self, user_id: int, data: datetime.date) -> int:
        pass

    async def get_user_shifts_for_current_month(self, user_id: int, year: int, month: int) -> List[UserShiftDetail]:
        if not (year and month):
            today = datetime.date.today()
            year, month = today.year, today.month

        try:
            shifts = await self.repository.get_user_shifts_by_date(
                user_id=user_id,
                year=year,
                month=month
            )
        except ItemNotFound:
            raise HTTPException(status_code=404, detail=f"No shifts found for user with ID {user_id}")

        return [self.detail_schema.model_validate(shift) for shift in shifts]

    async def get_list_shifts_for_current_month(self, year: int, month: int):
        shifts = await self.repository.get_list_shifts_for_current_month(year, month)

        if not shifts:
            raise HTTPException(status_code=404)

        return [self.detail_schema.model_validate(obj=obj) for obj in shifts]