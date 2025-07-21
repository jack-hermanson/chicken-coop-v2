from datetime import date, datetime, timedelta
from time import perf_counter

from application import db, logger
from application.modules.schedule.models import Shift, ShiftAssignment, TimeOfDayEnum
from application.utils.date_time import LOCAL_TIMEZONE


# Todo: add unit testing, change params to start and end date?
def generate_shifts(days_ahead: int = 365) -> None:
    """Generate shifts in advance"""
    start = perf_counter()

    # Get all of the shift assignments first.
    shift_assignments = ShiftAssignment.query.order_by(ShiftAssignment.day_of_week, ShiftAssignment.time_of_day).all()

    # Create a list of dates to check if there are shifts for.
    dates_to_check: list[date] = [
        (datetime.now(tz=LOCAL_TIMEZONE) + timedelta(days=day_ahead)).date() for day_ahead in range(days_ahead)
    ]

    # Get already-created shifts; will be used in the loop.
    existing_shifts_in_range: list[Shift] = (
        Shift.query.filter(Shift.date.in_(dates_to_check)).order_by(Shift.shift_id).all()
    )

    # Loop through dates that are in the range we want.
    created_shifts_count: int = 0
    logger.debug(f"dates_to_check {dates_to_check}")
    for date_to_check in dates_to_check:
        # Morning and evening.
        for time_of_day in list(TimeOfDayEnum):
            # Find the assignment for this shift: e.g., Wednesday nights. Should always exist.
            shift_assignment: ShiftAssignment = next(
                filter(
                    lambda sa: sa.day_of_week == date_to_check.weekday() and sa.time_of_day == time_of_day,
                    shift_assignments,
                ),
            )
            # Find an existing shift for this assignment: e.g., Wednesday, June 25. May not exist.
            existing_shift = next(
                filter(
                    lambda s: (
                        s.shift_assignment_id == shift_assignment.shift_assignment_id and s.date == date_to_check
                    ),
                    existing_shifts_in_range,
                ),
                None,
            )
            # If it exists, move on.
            if existing_shift is not None:
                continue

            # Shift does not exist. Create it.
            shift = _create_shift(shift_assignment, date_to_check)
            created_shifts_count += 1
            db.session.add(shift)
            # Shift has been added, not committed.
    db.session.commit()
    logger.info(f"Created {created_shifts_count} shifts in {perf_counter() - start} seconds")


def _create_shift(shift_assignment: ShiftAssignment, shift_date: date) -> Shift:
    """Create a Shift and return it; do not save it to db."""
    shift: Shift = Shift()
    shift.shift_assignment = shift_assignment
    shift.date = shift_date

    # no auto flush because the back reference to this nes shift does not work yet
    with db.session.no_autoflush:
        shift.assigned_to_account = shift_assignment.account
    return shift
