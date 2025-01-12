from sqlalchemy import Column, INT, VARCHAR, Text, UniqueConstraint

from src.models import Base


class ScheduleTemplate(Base):
    __tablename__ = "schedule_templates"
    __table_args__ = (
        UniqueConstraint("work_days", "rest_days"),     # todo: Need migrations(recreate db)
    )

    id = Column(INT, primary_key=True)
    name = Column(VARCHAR(16), nullable=False)
    work_days = Column(INT, nullable=False)
    rest_days = Column(INT, nullable=False)
    description = Column(Text, nullable=True)
