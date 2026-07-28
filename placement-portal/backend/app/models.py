from datetime import datetime
from app.extensions import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), nullable=False)

    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class StudentProfile(db.Model):

    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    student_id = db.Column(db.String(30), unique=True)

    phone = db.Column(db.String(15))

    branch = db.Column(db.String(50))

    cgpa = db.Column(db.Float)

    graduation_year = db.Column(db.Integer)

    resume = db.Column(db.String(255))

    is_placed = db.Column(db.Boolean, default=False)


class CompanyProfile(db.Model):

    __tablename__ = "company_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    company_name = db.Column(db.String(100), nullable=False)

    hr_name = db.Column(db.String(100))

    hr_email = db.Column(db.String(120))

    phone = db.Column(db.String(20))

    website = db.Column(db.String(255))

    description = db.Column(db.Text)

    approval_status = db.Column(
        db.String(20),
        default="pending"
    )

    is_blacklisted = db.Column(
        db.Boolean,
        default=False
    )

class PlacementDrive(db.Model):

    __tablename__ = "placement_drives"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("company_profiles.id"),
        nullable=False
    )

    job_title = db.Column(db.String(150), nullable=False)

    job_description = db.Column(db.Text)

    eligibility_branch = db.Column(db.String(100))

    minimum_cgpa = db.Column(db.Float)

    graduation_year = db.Column(db.Integer)

    application_deadline = db.Column(db.Date)

    status = db.Column(
        db.String(20),
        default="pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Application(db.Model):

    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student_profiles.id"),
        nullable=False
    )

    drive_id = db.Column(
        db.Integer,
        db.ForeignKey("placement_drives.id"),
        nullable=False
    )

    applied_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(30),
        default="applied"
    )
    __table_args__ = (
    db.UniqueConstraint(
        "student_id",
        "drive_id",
        name="unique_application"
    ),
    )

class Interview(db.Model):

    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)

    application_id = db.Column(
        db.Integer,
        db.ForeignKey("applications.id"),
        nullable=False
    )

    interview_date = db.Column(db.DateTime)

    interview_type = db.Column(db.String(50))

    status = db.Column(db.String(30))

    remarks = db.Column(db.Text)


class Notification(db.Model):

    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    message = db.Column(db.Text)

    is_read = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )



