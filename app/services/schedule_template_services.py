from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.abstract import AbstractRepository
from app.repositories.schedule_template_repositories import ScheduleTemplateRepositories
from app.schemas.schedule_templates import ScheduleTemplateCreateForm, ScheduleTemplateDetail, ScheduleTemplateEditForm
from src.exceptions import ItemNotFound, DuplicateEntryError


class ScheduleTemplateService(AbstractRepository):
    create_schema = ScheduleTemplateCreateForm
    edit_schema = ScheduleTemplateEditForm
    detail_schema = ScheduleTemplateDetail

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ScheduleTemplateRepositories(session=session)

    async def get(self, pk: int) -> detail_schema:
        try:
            obj = await self.repository.get(pk=pk)
        except ItemNotFound:
            raise HTTPException(status_code=404)
        return self.detail_schema.model_validate(obj=obj)

    async def update(self, pk: int, form: create_schema) -> detail_schema:
        data = form.model_dump(exclude_none=True)
        if not data:
            raise HTTPException(status_code=400, detail="No valid field for update.")
        try:
            obj = await self.repository.update(pk=pk, data=data)
        except ItemNotFound:
            raise HTTPException(status_code=404, detail="No template for update.")
        return self.detail_schema.model_validate(obj=obj)

    async def save(self, form: create_schema) -> detail_schema:
        try:
            obj = await self.repository.save(form=form.model_dump())
        except DuplicateEntryError:
            raise HTTPException(status_code=400, detail="Template with this work and rest days is exists")
        return self.detail_schema.model_validate(obj=obj)

    async def delete(self, *args, **kwargs):
        raise NotImplementedError

    async def list(self, *args, **kwargs) -> list[detail_schema]:
        try:
            objs = await self.repository.list()
        except Exception:
            raise HTTPException(status_code=404, detail="Unknown Error")
        return [self.detail_schema.model_validate(obj=obj) for obj in objs]
