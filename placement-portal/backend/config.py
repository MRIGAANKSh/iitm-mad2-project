import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = "placement-portal-secret-key"

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "placement.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "placement-portal-jwt-secret"

    UPLOAD_FOLDER = os.path.join(
    os.getcwd(),
    "uploads"
        )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024