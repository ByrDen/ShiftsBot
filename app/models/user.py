from sqlalchemy import Column, Integer, VARCHAR, Enum, ForeignKey, inspect, Date
from sqlalchemy.orm import relationship

from src.models import Base
from app.models.users_shifts import UsersShifts
from src.enums import UserRole


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, nullable=False)
    last_name = Column(VARCHAR(32), nullable=False)
    start_date = Column(Date, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE, nullable=False)

    shift_template_id = Column(ForeignKey("schedule_templates.id"), nullable=True)

    # shifts = relationship(
    #     argument="Shift",
    #     secondary=inspect(UsersShifts).local_table,
    #     back_populates="employees",
    #     lazy="noload"
    # )

