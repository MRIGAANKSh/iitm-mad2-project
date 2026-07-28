from flask import Flask

from config import Config

from app.extensions import db
from app.extensions import jwt
from app.extensions import cors


from app.auth import auth_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    jwt.init_app(app)

    cors.init_app(app)
    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():

        return {
            "message": "Placement Portal API is running"
        }

    return app