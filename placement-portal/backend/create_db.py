from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():

    print("Creating database...")

    db.create_all()

    admin = User.query.filter_by(
        email="admin@placement.com"
    ).first()

    if not admin:

        admin = User(
            name="Placement Admin",
            email="admin@placement.com",
            password=generate_password_hash("admin123"),
            role="admin"
        )

        db.session.add(admin)

        db.session.commit()

        print("Default admin created.")

    else:

        print("Admin already exists.")

    print("Database setup completed successfully.")