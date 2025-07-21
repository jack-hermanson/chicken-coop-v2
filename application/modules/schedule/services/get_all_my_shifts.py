from flask_login import current_user
from sqlalchemy import and_, desc, func

from application.modules.schedule.models import Shift, ShiftAssignment
from application.modules.schedule.view_models import ShiftViewModel
from application.utils.pagination import TypedPagination


def get_all_my_shifts(*, page: int, past: bool) -> TypedPagination[ShiftViewModel]:
    # Get shifts from db.
    paginated_shifts: TypedPagination[Shift] = (
        Shift.query.join(Shift.shift_assignment)
        .filter(
            and_(
                Shift.assigned_to_account_id == current_user.account_id,
                ((Shift.date < func.current_date()) if past else (Shift.date >= func.current_date())),
            ),
        )
        .order_by(
            (desc(Shift.date) if past else Shift.date),
            (desc(ShiftAssignment.time_of_day) if past else ShiftAssignment.time_of_day),
        )
        .paginate(page=page, per_page=10)
    )

    paginated_shifts.items = [
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
        for shift in paginated_shifts.items
    ]

    return paginated_shifts
