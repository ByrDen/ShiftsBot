__all__ = ["ScheduleTemplateRepositories"]

from app.models import ScheduleTemplate
from app.repositories.alchemy_repository import SQLAlchemyRepository


class ScheduleTemplateRepositories(SQLAlchemyRepository):
    model = ScheduleTemplate


