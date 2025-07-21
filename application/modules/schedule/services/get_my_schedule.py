from flask_login import current_user
from sqlalchemy import and_, desc, func

from application.modules.schedule.models import Shift, ShiftAssignment
from application.modules.schedule.view_models import MyScheduleViewModel, ShiftAssignmentViewModel, ShiftViewModel


def get_my_schedule() -> MyScheduleViewModel:
    """Get the user's upcoming and past shifts, and their weekly assignments."""

    next_shifts = _get_my_next_shifts()
    past_shifts = _get_my_past_shifts()
    weekly_assignments = _get_my_weekly_assignments()

    return MyScheduleViewModel(
        next_shifts=next_shifts,
        past_shifts=past_shifts,
        weekly_assignments=weekly_assignments,
    )


def _get_my_weekly_assignments() -> list[ShiftAssignmentViewModel]:
    """Get, sort, and package up the list of shift assignments for the current user."""
    shift_assignments: list[ShiftAssignment] = (
        ShiftAssignment.query.filter(ShiftAssignment.account_id == current_user.account_id)
        .order_by(ShiftAssignment.day_of_week, ShiftAssignment.time_of_day)
        .all()
    )

    return [
        ShiftAssignmentViewModel(
            shift_assignment_id=shift_assignment.shift_assignment_id,
            day_of_week=shift_assignment.day_of_week,
            time_of_day=shift_assignment.time_of_day,
        )
        for shift_assignment in shift_assignments
    ]


def _get_my_next_shifts(limit: int = 3) -> list[ShiftViewModel]:
    shifts: list[Shift] = (
        Shift.query.filter(
            and_(
                Shift.assigned_to_account_id == current_user.account_id,
                Shift.date >= func.current_date(),
            ),
        )
        .order_by(Shift.date)
        .limit(limit)
        .all()
    )
    return [
        ShiftViewModel(
            shift_id=shift.shift_id,
            shift_assignment_id=shift.shift_assignment_id,
            day_of_week=shift.shift_assignment.day_of_week,
            time_of_day=shift.shift_assignment.time_of_day,
            date=shift.date,
            comments=shift.comments,
            eggs_collected=shift.eggs_collected,
            eggs_left_behind=shift.eggs_left_behind,
            completed_by_account=shift.completed_by_account,
            completed_datetime_utc=shift.completed_datetime_utc,
        )
        for shift in shifts
    ]


def _get_my_past_shifts(limit: int = 3) -> list[ShiftViewModel]:
    shifts: list[Shift] = (
        Shift.query.join(Shift.shift_assignment)
        .filter(
            Shift.assigned_to_account_id == current_user.account_id,
            Shift.date < func.current_date(),
        )
        .order_by(desc(Shift.date), desc(ShiftAssignment.time_of_day))
        .limit(limit)
        .all()
    )

    return [
        ShiftViewModel(
            shift_id=shift.shift_id,
            shift_assignment_id=shift.shift_assignment_id,
            day_of_week=shift.shift_assignment.day_of_week,
            time_of_day=shift.shift_assignment.time_of_day,
            date=shift.date,
            comments=shift.comments,
            eggs_collected=shift.eggs_collected,
            eggs_left_behind=shift.eggs_left_behind,
            completed_by_account=shift.completed_by_account,
            completed_datetime_utc=shift.completed_datetime_utc,
        )
        for shift in shifts
    ]
