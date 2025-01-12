import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, ConfigDict

from src.enums import UserRole


class UserCreateForm(BaseModel):
    tg_id: PositiveInt = Field(default=..., description="Telegram ID пользователя")
    last_name: str = Field(default=..., min_length=2, max_length=32, description="Фамилия пользователя")
    role: UserRole = Field(default=UserRole.EMPLOYEE, description="Роль пользователя")
    start_date: Optional[datetime.date] = Field(default=None)
    shift_template_id: Optional[PositiveInt] = Field(
        default=None, description="Шаблон смен для пользователя"
    )


class UserEditForm(BaseModel):
    last_name: Optional[str] = Field(default=None, min_length=2, max_length=32, description="Роль пользователя")
    role: Optional[UserRole] = Field(default=None, description="Роль пользователя")
    shift_template_id: Optional[PositiveInt] = Field(
        default=None, description="Шаблон смен для пользователя"
    )


class UserDetail(UserCreateForm):
    id: PositiveInt

    model_config = ConfigDict(from_attributes=True)
