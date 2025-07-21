from time import perf_counter

from application import create_app
from application.modules.schedule.models import DayOfWeekEnum, Shift

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        start = perf_counter()
        data = Shift.query.filter(Shift.assigned_to_account_id == 1).all()
        for shift in data:
            x = f"{shift.shift_id} is on {shift.date.isoformat()} - {DayOfWeekEnum(shift.shift_assignment.day_of_week).name}"
        stop = perf_counter()
        print(stop - start)
