from datetime import date
from enum import IntEnum
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application import db

if TYPE_CHECKING:
    from application.modules.accounts.models import Account


class Shift(db.Model):
    __tablename__ = "shift"

    shift_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    comments: Mapped[str] = mapped_column(String(255), nullable=False, server_default="", default="")
    eggs_collected: Mapped[int] = mapped_column(Integer, nullable=True)
    eggs_left_behind: Mapped[int] = mapped_column(Integer, nullable=True)

    # Relationship back to Account for list of assigned shifts
    assigned_to_account_id: Mapped[int] = mapped_column(ForeignKey("account.account_id"), nullable=True)
    assigned_to_account: Mapped["Account"] = relationship(back_populates="assigned_shifts", lazy="select")

    # If this shift has a coverage request
    coverage_request: Mapped["CoverageRequest"] = relationship(back_populates="shift", uselist=False)

    # Relationship back to ShiftAssignment for list of specific shifts
    shift_assignment_id: Mapped[int] = mapped_column(ForeignKey("shift_assignment.shift_assignment_id"), nullable=True)
    shift_assignment: Mapped["ShiftAssignment"] = relationship(back_populates="shifts", lazy="select")


class CoverageRequest(db.Model):
    __tablename__ = "coverage_request"

    coverage_request_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Relationship back to Shift
    shift_id: Mapped[int] = mapped_column(ForeignKey("shift.shift_id"), nullable=False, unique=True)
    shift: Mapped["Shift"] = relationship(back_populates="coverage_request", lazy="select")

    # Covered by


class TimeOfDayEnum(IntEnum):
    MORNING = 1
    EVENING = 2


class DayOfWeekEnum(IntEnum):
    """Starting at 0 for Monday because date.today().weekday() returns 0 for Monday"""

    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class ShiftAssignment(db.Model):
    __tablename__ = "shift_assignment"

    shift_assignment_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    time_of_day: Mapped[TimeOfDayEnum] = mapped_column(Integer, nullable=False)
    day_of_week: Mapped[DayOfWeekEnum] = mapped_column(Integer, nullable=False)

    # Relationship back to Account for list of assigned shifts
    account_id: Mapped[int] = mapped_column(ForeignKey("account.account_id"), nullable=True)
    account: Mapped["Account"] = relationship(back_populates="assignments", lazy="select")

    # Children
    shifts: Mapped[list["Shift"]] = relationship(
        back_populates="shift_assignment",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    # completed_datetime_utc: Mapped[datetime] = mapped_column(
    #     DateTime(timezone=True),
    #     nullable=False,
    #     default=utcnow,
    #     server_default=text("CURRENT_TIMESTAMP"),
    # )
