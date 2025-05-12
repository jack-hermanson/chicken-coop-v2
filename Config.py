import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    pass
    # TEMPLATES_AUTO_RELOAD = bool(int(os.getenv("TEMPLATES_AUTO_RELOAD")))
    # SECRET_KEY = os.getenv("SECRET_KEY")
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # if os.environ.get("DATABASE_URL"):
    #     SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace("postgres://", "postgresql://")
    # else:
    #     SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    # SQLALCHEMY_ECHO = bool(int(os.getenv("SQLALCHEMY_ECHO", "0")))
