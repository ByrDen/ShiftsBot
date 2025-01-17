__all__ = ["UsersShifts"]

import datetime
from typing import Optional

from sqlalchemy import Column, INT, ForeignKey, Enum, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base
from src.enums import ShiftType


class UsersShifts(Base):
    __tablename__ = "users_shift"
    __table_args__ = (
        UniqueConstraint("user_id", "date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="users.id",
            ondelete="CASCADE",
            onupdate="RESTRICT",
        ),
        index=True
    )
    date: Mapped[datetime.date] = mapped_column(index=True)
    shift_template_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(
            column="schedule_templates.id",
            ondelete="CASCADE",
            onupdate="RESTRICT",
        )
    )
    shift_type: Mapped[ShiftType] = mapped_column(default=ShiftType.SCHEDULE, index=True)

    def __repr__(self) -> str:
        return f"{self.id=}\n{self.user_id=}\n{self.date=}\n{self.shift_template_id=}\n{self.shift_type=}"


# class UsersShifts(Base):
#     __tablename__ = "users_shift"
#     __table_args__ = (
#         UniqueConstraint("user_id", "date"),
#     )
#     id = Column(INT, primary_key=True)
#     user_id = Column(
#         INT,
#         ForeignKey(
#             column="users.id",
#             ondelete="CASCADE",
#             onupdate="RESTRICT",
#         ),
#         nullable=False,
#         index=True
#     )
#
#     date = Column(Date, nullable=False, index=True)
#     shift_template_id = Column(
#         INT,
#         ForeignKey("schedule_templates.id"),
#         nullable=True,
#     )
#     shift_type = Column(
#         Enum(ShiftType),
#         default=ShiftType.SCHEDULE,
#         server_default='SCHEDULE',
#         nullable=False,
#         index=True
#     )
#
#     def __repr__(self) -> str:
#         return f"{self.id=}\n{self.user_id=}\n{self.date=}\n{self.shift_template_id=}\n{self.shift_type=}"
