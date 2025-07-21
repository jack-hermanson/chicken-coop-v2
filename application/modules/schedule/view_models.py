from dataclasses import dataclass
from datetime import date, datetime

from application.modules.accounts.models import Account
from application.modules.schedule.models import DayOfWeekEnum, TimeOfDayEnum
from application.utils.date_time import LOCAL_TIMEZONE


@dataclass
class ShiftViewModel:
    shift_id: int
    shift_assignment_id: int
    day_of_week: DayOfWeekEnum
    time_of_day: TimeOfDayEnum
    date: date
    comments: str
    eggs_collected: int | None
    eggs_left_behind: int | None
    completed_datetime_utc: datetime | None
    completed_by_account: Account | None

    @property
    def is_today(self) -> bool:
        return self.date == datetime.now(tz=LOCAL_TIMEZONE).date()


@dataclass
class ShiftAssignmentViewModel:
    shift_assignment_id: int
    day_of_week: DayOfWeekEnum
    time_of_day: TimeOfDayEnum


@dataclass
class MyScheduleViewModel:
    next_shifts: list[ShiftViewModel]
    past_shifts: list[ShiftViewModel]
    weekly_assignments: list[ShiftAssignmentViewModel]
