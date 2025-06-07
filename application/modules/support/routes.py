from flask import Blueprint, render_template
from flask.typing import ResponseReturnValue

support = Blueprint("support", __name__, url_prefix="/support")


@support.route("/")
def index() -> ResponseReturnValue:
    return render_template("support/index.html")
