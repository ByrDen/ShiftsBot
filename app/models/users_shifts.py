__all__ = ["UsersShifts"]
from sqlalchemy import Column, INT, ForeignKey, Enum, Date, UniqueConstraint

from src.models import Base
from src.enums import ShiftType


class UsersShifts(Base):
    __tablename__ = "users_shift"
    __table_args__ = (
        UniqueConstraint("user_id", "date"),
    )
    id = Column(INT, primary_key=True)
    user_id = Column(
        INT,
        ForeignKey(
            column="users.id",
            ondelete="CASCADE",
            onupdate="RESTRICT",
        ),
        nullable=False,
        index=True
    )

    date = Column(Date, nullable=False, index=True)
    shift_template_id = Column(
        INT,
        ForeignKey("schedule_templates.id"),
        nullable=True,
    )
    shift_type = Column(
        Enum(ShiftType),
        default=ShiftType.SCHEDULE,
        server_default="schedule",
        nullable=False,
        index=True
    )
