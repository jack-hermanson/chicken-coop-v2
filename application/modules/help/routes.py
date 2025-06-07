from flask import Blueprint, render_template
from flask.typing import ResponseReturnValue

help = Blueprint("help", __name__, url_prefix="/help")


@help.route("/")
def index() -> ResponseReturnValue:
    return render_template("help/index.html")
