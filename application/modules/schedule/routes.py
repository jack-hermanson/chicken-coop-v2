from flask import Blueprint, render_template, request
from flask.typing import ResponseReturnValue

from application import ClearanceEnum
from application.modules.accounts.requires_clearance import requires_clearance
from application.modules.schedule.services.get_all_my_shifts import get_all_my_shifts
from application.modules.schedule.services.get_my_schedule import get_my_schedule

schedule = Blueprint("schedule", __name__, url_prefix="/schedule")


@schedule.route("/")
@requires_clearance(ClearanceEnum.NORMAL)
def my_schedule() -> ResponseReturnValue:
    """Dashboard page for your shifts. Shows what is next."""
    return render_template("schedule/my_schedule.html", my_schedule=get_my_schedule())


@schedule.route("/more")
@requires_clearance(ClearanceEnum.NORMAL)
def all_my_shifts() -> ResponseReturnValue:
    """Paginated list of shifts."""
    # Get info from request.
    page = request.args.get("page", type=int, default=1)
    past = request.args.get("past", type=str, default="false").lower() == "true"

    paginated_shifts = get_all_my_shifts(page=page, past=past)
    return render_template("schedule/all_my_shifts.html", paginated_shifts=paginated_shifts, page=page, past=past)


@schedule.route("/daily")
@requires_clearance(ClearanceEnum.NORMAL)
def daily() -> ResponseReturnValue:
    return render_template("schedule/daily.html")


@schedule.route("/weekly")
@requires_clearance(ClearanceEnum.NORMAL)
def weekly() -> ResponseReturnValue:
    return render_template("schedule/weekly.html")
