from typing import Optional

from sqlalchemy import Column, INT, VARCHAR, Text, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from src.models import Base


class ScheduleTemplate(Base):
    __tablename__ = "schedule_templates"
    __table_args__ = (
        UniqueConstraint("work_days", "rest_days"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(16))
    work_days: Mapped[int]
    rest_days: Mapped[int]
    description: Mapped[Optional[str]] = mapped_column(VARCHAR(128))


# class ScheduleTemplate(Base):
#     __tablename__ = "schedule_templates"
#     __table_args__ = (
#         UniqueConstraint("work_days", "rest_days"),
#     )
#
#     id = Column(INT, primary_key=True)
#     name = Column(VARCHAR(16), nullable=False)
#     work_days = Column(INT, nullable=False)
#     rest_days = Column(INT, nullable=False)
#     description = Column(Text, nullable=True)
