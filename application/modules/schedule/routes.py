from flask import Blueprint, render_template
from flask.typing import ResponseReturnValue

schedule = Blueprint("schedule", __name__, url_prefix="/schedule")


@schedule.route("/")
def index() -> ResponseReturnValue:
    return render_template("schedule/index.html")
