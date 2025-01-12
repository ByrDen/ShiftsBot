__all__ = ["UserService"]
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.abstract import AbstractRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserDetail, UserEditForm, UserCreateForm
from src.exceptions import ItemNotFound, DuplicateEntryError, UserNotFound


class UserService(AbstractRepository):

    create_schema = UserCreateForm
    edit_schema = UserEditForm
    detail_schema = UserDetail

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = UserRepository(session=session)

    async def get(self, pk: int) -> detail_schema:
        try:
            obj = await self.repository.get(pk=pk)
        except ItemNotFound:
            raise HTTPException(status_code=404, detail=f"User with id:{pk} not found.")
        return self.detail_schema.model_validate(obj=obj)

    async def update(self, pk: int, form: create_schema) -> detail_schema:
        data = form.model_dump(exclude_none=True)
        if not data:
            raise HTTPException(status_code=400, detail="No valid field for update.")
        try:
            obj = await self.repository.update(pk=pk, data=data)
        except ItemNotFound:
            raise HTTPException(status_code=404, detail=f"User with id:{pk} not found.")
        return self.detail_schema.model_validate(obj=obj)

    async def save(self, form: create_schema) -> detail_schema:
        try:
            obj = await self.repository.save(form=form.model_dump())
        except DuplicateEntryError as e:
            raise HTTPException(status_code=422, detail=e)
        return self.detail_schema.model_validate(obj=obj)

    async def delete(self, pk: int):
        return await self.repository.delete(pk=pk)

    async def list(self, *args, **kwargs) -> Sequence[detail_schema]:
        objs = await self.repository.list(**kwargs)
        return [self.detail_schema.model_validate(obj=obj) for obj in objs]

    async def get_pk_by_tg_id(self, tg_id: int) -> int:
        try:
            pk = await self.repository.get_pk_by_field(field_name="tg_id", value=tg_id)
        except UserNotFound:
            raise HTTPException(status_code=404)
        return pk[0]
