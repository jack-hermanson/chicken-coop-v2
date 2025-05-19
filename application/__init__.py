import os
import subprocess

from flask import Flask, request

from Config import Config
from utils.get_ip import get_ip


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path="/static", static_folder="web/static", template_folder="web/templates")

    app.config.from_object(config_class)

    @app.context_processor
    def inject_environment():
        return dict(
            commit=subprocess.check_output(["git", "describe", "--always"]).strip().decode("utf-8"),
            environment=os.environ.get("ENVIRONMENT"),
            # get_ip=get_ip
        )

    # todo - remove this
    @app.route("/")
    def index():
        # return "hi"
        return f"""
        <html style="background-color: #222; color: #ddd; font-family: sans-serif;">
        <body>
        <h1>Hi {get_ip(request=request)}</h1>
        </body>
        </html>
        """

    print("RUNNING APPLICATION")
    return app