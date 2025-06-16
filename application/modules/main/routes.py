from pathlib import Path

from flask import Blueprint, redirect, render_template, send_file, url_for
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


@main.route("/info")
def info() -> ResponseReturnValue:
    return redirect(url_for("about.index"), code=301)


@main.route("/error-500")
def error_500() -> ResponseReturnValue:
    raise ValueError("Error on purpose")


@main.route("/manifest.json")
def serve_manifest() -> ResponseReturnValue:
    path = Path("./application/web/static/manifest.json")
    return send_file(path.resolve(strict=True), mimetype="application/manifest+json")


@main.route("/sw.js")
def serve_sw() -> ResponseReturnValue:
    path = Path("./application/web/static/sw.js")
    return send_file(path.resolve(strict=True), mimetype="application/javascript")
