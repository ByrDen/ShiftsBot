__all__ = ["UserRole", "ShiftType"]
import enum


class UserRole(enum.Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"


class ShiftType(enum.Enum):
    SCHEDULE = "schedule"
    EXTRA_WORK = "extra_work"
