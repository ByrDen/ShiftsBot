import datetime

from pydantic import BaseModel, PositiveInt, ConfigDict


class SpecificShiftDayCreateForm(BaseModel):
    date: datetime.date
    max_employees: PositiveInt
    shift_limit_id: PositiveInt


class SpecificShiftDayEditForm(SpecificShiftDayCreateForm):
    ...


class SpecificShiftDayDetail(SpecificShiftDayEditForm):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt

