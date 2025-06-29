from sqlalchemy import and_

from application import db, logger
from application.modules.shifts.models import DayOfWeekEnum, ShiftAssignment, TimeOfDayEnum


def seed_shift_assignments() -> None:
    """
    Seed the db with the ShiftAssignments for every day of the week.
    """

    created_shift_assignments_count: int = 0

    # for each day, check if a shift for each time, and create it if not
    for day_of_week in DayOfWeekEnum:
        for time_of_day in TimeOfDayEnum:
            # see if this shift assignment already exists
            shift_assignment = ShiftAssignment.query.filter(
                and_(
                    ShiftAssignment.time_of_day == time_of_day,
                    ShiftAssignment.day_of_week == day_of_week,
                ),
            ).first()
            if shift_assignment:
                # logger.debug(
                #     f"Shift assignment for {day_of_week.name} {time_of_day.name} already exists with id "
                #     f"{shift_assignment.shift_assignment_id}",
                # )
                continue

            # it does not exist, so create it
            logger.debug(f"Shift assignment for {day_of_week.name} {time_of_day.name} does not exist")
            shift_assignment = ShiftAssignment()
            shift_assignment.time_of_day = time_of_day
            shift_assignment.day_of_week = day_of_week
            shift_assignment.seeking_permanent_replacement = False
            db.session.add(shift_assignment)
            logger.debug(f"Created {shift_assignment}")
            created_shift_assignments_count += 1

    db.session.commit()
    logger.debug(f"Done. Created {created_shift_assignments_count} shift assignments.")
