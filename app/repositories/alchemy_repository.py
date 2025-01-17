__all__ = ["SQLAlchemyRepository"]
from typing import Any, Type, Sequence
from pydantic import BaseModel
from sqlalchemy import select, inspect, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapper, selectinload

from app.repositories.abstract import AbstractRepository
from src.exceptions import ItemNotFound, DuplicateEntryError, RepositoryError


class SQLAlchemyRepository(AbstractRepository):
    model: Type[Mapper]

    def __init__(self, session: AsyncSession):
        self.session = session
        self.mapper: Mapper = inspect(self.model)
        self.pk = self.mapper.primary_key[0]
        self.relationships = self.mapper.relationships

    async def _run_query(self, statement):
        try:
            return await self.session.execute(statement=statement)
        except IntegrityError as e:
        # except Exception as e:
        #     raise RepositoryError from e
            # await self.session.rollback()
            if "unique constraint" in str(e).lower():
                raise DuplicateEntryError("A unique constraint was violated.") from e
            if "foreign key constraint" in str(e).lower():
                raise RepositoryError("Error from foreign key") from e
            if "is not present in table" in str(e).lower():
                raise ItemNotFound("Item with this id no found") from e
            # raise UnknownError from e

    async def get(self, pk: Any) -> Mapper:
        stmt = select(self.model).filter(self.pk == pk)

        for relationship in self.relationships:
            stmt = stmt.options(selectinload(relationship))
        result = await self._run_query(statement=stmt)
        obj = result.unique().scalar_one_or_none()
        if not obj:
            raise ItemNotFound(f"Object with id:{pk} not found.")
        return obj

    async def get_pk_by_field(self, field_name: str, value: Any):
        stmt = select(self.pk).filter(getattr(self.model, field_name) == value)
        result = await self._run_query(statement=stmt)
        return result.scalars().unique().all()

    async def get_by_field(self, field_name: str, value: Any) -> Sequence[Mapper]:
        stmt = select(self.model).filter(getattr(self.model, field_name) == value)
        result = await self._run_query(statement=stmt)
        return result.scalars().unique().all()

    async def update(self, pk: Any, data: dict[str, Any]) -> Sequence[Mapper]:  # todo: check update
        stmt = update(self.model).where(self.pk == pk).values(**data).returning(self.model)
        result = await self._run_query(statement=stmt)
        updated_obj = result.scalars().unique().one_or_none()
        if not updated_obj:
            raise ItemNotFound("Object not found to update")
        await self.session.commit()
        return updated_obj

    async def save(self, form: dict[str, Any]) -> Mapper:
        obj = self.model(**form)
        self.session.add(obj)
        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise DuplicateEntryError("Duplicate entry detected.") from e
        await self.session.refresh(instance=obj)
        return obj

    async def delete(self, pk: Any) -> None:
        stmt = delete(self.model).filter(self.pk == pk)
        await self.session.execute(statement=stmt)
        await self.session.commit()

    async def list(
            self,
            order_by: str = None,
            order: str = None,
            limit: int = None,
            offset: int = None,
            **kwargs
    ) -> Sequence[Mapper]:
        stmt = select(self.model)
        if order and order_by:
            stmt = stmt.order_by(getattr(getattr(self.model, order_by), order))
        stmt = stmt.limit(limit=limit).offset(offset=offset)
        if kwargs:
            stmt = stmt.filter_by(**kwargs)
        objs = await self._run_query(statement=stmt)
        return objs.unique().scalars().all()
