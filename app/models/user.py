import datetime
from typing import Optional

from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.models import Base
from app.models.users_shifts import UsersShifts
from src.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(unique=True)
    last_name: Mapped[str] = mapped_column(VARCHAR(32))
    start_date: Mapped[Optional[datetime.date]]
    role: Mapped[UserRole] = mapped_column(default=UserRole.EMPLOYEE)

    shift_template_id: Mapped[Optional[int]] = mapped_column(ForeignKey("schedule_templates.id"))

    def __repr__(self):
        return (f"{self.id=}\n{self.tg_id=}\n{self.last_name=}\n"
                f"{self.start_date=}\n {self.role=}\n{self.shift_template_id=}")
    # shifts: Mapped[UsersShifts] = relationship(
    #
    # )


# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     tg_id = Column(Integer, unique=True, nullable=False)
#     last_name = Column(VARCHAR(32), nullable=False)
#     start_date = Column(Date, nullable=True)
#     role = Column(Enum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
#
#     shift_template_id = Column(ForeignKey("schedule_templates.id"), nullable=True)

    # shifts = relationship(
    #     argument="Shift",
    #     secondary=inspect(UsersShifts).local_table,
    #     back_populates="employees",
    #     lazy="noload"
    # )

