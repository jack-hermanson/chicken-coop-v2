from flask import Flask

from Config import Config


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path="/static", static_folder="web/static", template_folder="web/templates")

    app.config.from_object(config_class)

    @app.route("/")
    def index():
        return "hi"
        return "<body style='background-color: #222; color: #eee;>hello</body>'"

    print("RUNNING APPLICATION")
    return app