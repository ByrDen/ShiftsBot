__all__ = ["router"]
from fastapi import APIRouter

from app.schemas.schedule_templates import ScheduleTemplateDetail, ScheduleTemplateCreateForm
from app.services.schedule_template_services import ScheduleTemplateService
from src.database import DBSession

router = APIRouter(
    prefix="/template",
    tags=["Template"]
)


@router.get(path="", response_model=list[ScheduleTemplateDetail])
async def get_list_templates(session: DBSession):
    return await ScheduleTemplateService(session=session).list()


@router.post(path="", response_model=ScheduleTemplateDetail, status_code=201)
async def create_template(
        session: DBSession,
        form: ScheduleTemplateCreateForm
):
    return await ScheduleTemplateService(session=session).save(form=form)

