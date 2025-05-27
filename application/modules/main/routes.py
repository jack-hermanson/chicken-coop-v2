from flask import Blueprint, render_template
from flask.typing import ResponseReturnValue
from flask_login import current_user

from application import ClearanceEnum, logger

main = Blueprint("main", __name__, url_prefix="")


@main.route("/")
def index() -> ResponseReturnValue:
    if not current_user.is_authenticated or current_user.clearance <= ClearanceEnum.UNVERIFIED:
        logger.debug("Not logged in / verified - showing about page instead of dashboard")
        return render_template("about/index.html")
    return render_template("main/index.html")
