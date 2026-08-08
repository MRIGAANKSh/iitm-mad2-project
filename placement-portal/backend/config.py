
import os

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


class Config:

    SECRET_KEY = "placement-portal-secret-key"

    CACHE_TYPE = "RedisCache"

    CACHE_REDIS_URL = "redis://localhost:6379/1"

    CACHE_DEFAULT_TIMEOUT = 300

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    MAIL_USERNAME = "23f2003457@ds.study.iitm.ac.in"
    MAIL_PASSWORD = "intj bdag nrhx iqwk"

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///"
        + os.path.join(
            BASE_DIR,
            "instance",
            "placement.db"
        )
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "placement-portal-jwt-secret"

    # Resume upload folder
    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads"
    )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

