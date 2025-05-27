from flask import Blueprint, render_template
from flask.typing import ResponseReturnValue

about = Blueprint("about", __name__, url_prefix="/about")


@about.route("/")
def index() -> ResponseReturnValue:
    return render_template("about/index.html")
