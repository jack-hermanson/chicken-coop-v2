from datetime import date, datetime
from enum import IntEnum
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application import db
from application.utils.date_time import utcnow

if TYPE_CHECKING:
    from application.modules.accounts.models import Account


class Shift(db.Model):
    """
    This is the individual instance of a shift, like the 6/19 evening shift.
    Should be generated a year in advance.
    """

    __tablename__ = "shift"

    shift_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    comments: Mapped[str] = mapped_column(String(255), nullable=False, server_default="", default="")
    eggs_collected: Mapped[int] = mapped_column(Integer, nullable=True)
    eggs_left_behind: Mapped[int] = mapped_column(Integer, nullable=True)
    # completed_datetime_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationship back to Account for list of assigned shifts
    assigned_to_account_id: Mapped[int] = mapped_column(ForeignKey("account.account_id"), nullable=True)
    assigned_to_account: Mapped["Account"] = relationship(back_populates="assigned_shifts", lazy="select")

    # If this shift has a coverage request
    coverage_request: Mapped["CoverageRequest"] = relationship(back_populates="shift", uselist=False)

    # Relationship back to ShiftAssignment for list of specific shifts
    shift_assignment_id: Mapped[int] = mapped_column(ForeignKey("shift_assignment.shift_assignment_id"), nullable=True)
    shift_assignment: Mapped["ShiftAssignment"] = relationship(back_populates="shifts", lazy="select")


class CoverageRequest(db.Model):
    """
    This has a one-to-one relationship with Shift.
    If a shift has a coverage request, this is it.
    If not, this does not exist.
    """

    __tablename__ = "coverage_request"

    coverage_request_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # When was this coverage request created
    created_datetime_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # Any notes the requestor wants to add
    comments: Mapped[str] = mapped_column(String(255), nullable=False, server_default="", default="")

    # Relationship back to Shift
    shift_id: Mapped[int] = mapped_column(ForeignKey("shift.shift_id"), nullable=False, unique=True)
    shift: Mapped["Shift"] = relationship(back_populates="coverage_request", lazy="select")

    # Covered by
    covered_by_account_id: Mapped[int] = mapped_column(ForeignKey("account.account_id"), nullable=True)
    covered_by_account: Mapped["Account"] = relationship(back_populates="accepted_coverage_requests", lazy="select")


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
    """
    This is a generic "assignment" that can have an account or not. Ex: "Monday evening". If there's an account,
    then Shifts will be generated for that person.
    When the assignment changes, all future Shifts should be updated to reflect that.
    """

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
