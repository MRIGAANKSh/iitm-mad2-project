from datetime import date, timedelta

from app.celery_app import celery

from app.models import (
    PlacementDrive,
    StudentProfile,
    Notification,
    User
)

from app.extensions import db


@celery.task
def send_deadline_reminders():

    today = date.today()

    reminder_date = today + timedelta(days=3)

    drives = PlacementDrive.query.filter(
        PlacementDrive.status == "approved",
        PlacementDrive.application_deadline >= today,
        PlacementDrive.application_deadline <= reminder_date
    ).all()

    students = StudentProfile.query.join(
        User,
        StudentProfile.user_id == User.id
    ).filter(
        User.is_active == True
    ).all()

    notifications_created = 0

    for drive in drives:

        for student in students:

            message = (
                f"Reminder: {drive.job_title} "
                f"has an application deadline on "
                f"{drive.application_deadline}."
            )

            notification = Notification(
                user_id=student.user_id,
                message=message
            )

            db.session.add(notification)

            notifications_created += 1

    db.session.commit()

    return {
        "status": "completed",
        "drives_found": len(drives),
        "notifications_created": notifications_created
    }