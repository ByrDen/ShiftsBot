import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, Field, ConfigDict

from app.schemas.user import UserDetail
from src.enums import ShiftType


class UserShiftCreateForm(BaseModel):
    # user_id: PositiveInt = Field(default=...,)
    date: datetime.date = Field(default=...,)
    shift_template_id: Optional[PositiveInt] = Field(default=None)
    shift_type: ShiftType = Field(default=ShiftType.SCHEDULE,)


class UserShiftEditForm(UserShiftCreateForm):
    ...


class UserShiftDetail(UserShiftCreateForm):
    model_config = ConfigDict(from_attributes=True)

    user_id: Optional[PositiveInt] = Field(default=None)
    users: Optional[list[UserDetail]] = Field(default=None)
    id: PositiveInt


