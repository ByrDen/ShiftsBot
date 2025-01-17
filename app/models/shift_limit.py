import datetime

from sqlalchemy import Column, Integer, Date, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class ShiftLimit(Base):
    __tablename__ = "shift_limit"
    __table_args__ = (
        UniqueConstraint("year", "month"),
        CheckConstraint(sqltext="year > 2000", name="year_more_2000"),
        CheckConstraint(sqltext="month > 0", name="valid_month_ge_1"),
        CheckConstraint(sqltext="month < 13", name="valid_month_le_12"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int]
    month: Mapped[int]
    max_employees: Mapped[int]


# class ShiftLimit(Base):
#     __tablename__ = "shift_limit"
#     __table_args__ = (
#         UniqueConstraint("year", "month"),
#         CheckConstraint(sqltext="year > 2000", name="year_more_2000"),
#         CheckConstraint(sqltext="month > 0", name="valid_month_ge_1"),
#         CheckConstraint(sqltext="month < 13", name="valid_month_le_12"),
#     )
#
#     id = Column(Integer, primary_key=True)
#     year = Column(Integer, nullable=False)
#     month = Column(Integer, nullable=False)
#     max_employees = Column(Integer, nullable=False)


class SpecificShiftDay(Base):
    __tablename__ = "specific_shift_days"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(unique=True)
    max_employees: Mapped[int]
    shift_limit_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="shift_limit.id",
            ondelete="CASCADE"
        )
    )


# class SpecificShiftDay(Base):
#     __tablename__ = "specific_shift_days"
#
#     id = Column(Integer, primary_key=True)
#     date = Column(Date, nullable=False, unique=True)
#     max_employees = Column(Integer, nullable=False)
#     shift_limit_id = Column(Integer, ForeignKey("shift_limit.id", ondelete="CASCADE"))
