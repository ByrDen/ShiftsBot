from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, ConfigDict


class ScheduleTemplateCreateForm(BaseModel):
    name: str = Field(default=..., description="Название графика")
    work_days: PositiveInt = Field(default=..., description="Количество рабочих дней")
    rest_days: PositiveInt = Field(default=..., description="Количество выходных дней")
    description: Optional[str] = Field(description="Описание смены")

    class Config:
        schem_extra = {
            "example": {
                "name": "2/2",
                "work_days": 2,
                "rest_days": 2,
                "description": "График для чередования двух рабочих дней с двумя выходными"
            }
        }


class ScheduleTemplateEditForm(ScheduleTemplateCreateForm):
    id: PositiveInt
    name: Optional[str] = Field(default=None, description="Название графика")
    work_days: Optional[PositiveInt] = Field(default=None, description="Количество рабочих дней")
    rest_days: Optional[PositiveInt] = Field(default=None, description="Количество выходных дней")
    description: Optional[str] = Field(default=None, description="Описание смены")


class ScheduleTemplateDetail(ScheduleTemplateCreateForm):
    id: PositiveInt
    model_config = ConfigDict(from_attributes=True)

