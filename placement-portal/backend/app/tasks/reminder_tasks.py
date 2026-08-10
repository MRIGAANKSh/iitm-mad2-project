from datetime import date, timedelta

from app.celery_app import celery

from app.models import (
    PlacementDrive,
    StudentProfile,
    Notification,
    User
)

from app.extensions import db

from app.email_sender import send_email


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
    emails_sent = 0
    emails_failed = 0

    for drive in drives:

        for student in students:

            student_user = User.query.get(student.user_id)

            message = (
                f"Reminder: {drive.job_title} "
                f"has an application deadline on "
                f"{drive.application_deadline}."
            )

            # Create portal notification
            notification = Notification(
                user_id=student.user_id,
                message=message
            )

            db.session.add(notification)

            notifications_created += 1

            # Send email
            try:

                send_email(
                    recipient=student_user.email,

                    subject="Placement Drive Deadline Reminder",

                    html_content=f"""
                    <html>
                        <body>

                            <h2>
                                Placement Drive Deadline Reminder
                            </h2>

                            <p>
                                Hello {student_user.name},
                            </p>

                            <p>
                                {message}
                            </p>

                            <p>
                                Please log in to the Placement Portal
                                to apply before the deadline.
                            </p>

                            <p>
                                Placement Cell
                            </p>

                        </body>
                    </html>
                    """
                )

                emails_sent += 1

            except Exception as e:

                emails_failed += 1

                print(
                    f"Email failed for "
                    f"{student_user.email}: {e}"
                )

    db.session.commit()

    return {
        "status": "completed",
        "drives_found": len(drives),
        "notifications_created": notifications_created,
        "emails_sent": emails_sent,
        "emails_failed": emails_failed
    }