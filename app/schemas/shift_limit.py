import datetime

from pydantic import BaseModel, Field, PositiveInt, ConfigDict


class ShiftLimitCreateForm(BaseModel):
    year: PositiveInt = Field(default=lambda: datetime.date.today().year, ge=2000, le=2100)
    month: PositiveInt = Field(default=lambda: datetime.date.today().month, ge=1, le=12)
    max_employees: PositiveInt = Field(default=6)


class ShiftLimitEditForm(ShiftLimitCreateForm):
    ...


class ShiftLimitDetail(ShiftLimitCreateForm):
    id: PositiveInt

    model_config = ConfigDict(from_attributes=True)
    