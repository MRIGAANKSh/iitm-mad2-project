import csv
import os

from app.celery_app import celery
from app.models import (
    Application,
    StudentProfile,
    PlacementDrive,
    CompanyProfile,
    Notification
)


@celery.task
def export_student_applications(student_id):

    student = StudentProfile.query.get(student_id)

    if not student:
        return {
            "status": "failed",
            "message": "Student not found"
        }

    applications = Application.query.filter_by(
        student_id=student_id
    ).all()

    export_folder = "exports"

    os.makedirs(
        export_folder,
        exist_ok=True
    )

    filename = f"student_{student_id}_applications.csv"

    filepath = os.path.join(
        export_folder,
        filename
    )

    with open(
        filepath,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Student ID",
            "Company Name",
            "Drive Title",
            "Application Status",
            "Application Date"
        ])

        for application in applications:

            drive = PlacementDrive.query.get(
                application.drive_id
            )

            company = CompanyProfile.query.get(
                drive.company_id
            )

            writer.writerow([
                student.student_id,
                company.company_name,
                drive.job_title,
                application.status,
                application.applied_at
            ])

    notification = Notification(
        user_id=student.user_id,
        message="Your application history export has been completed."
    )

    from app.extensions import db

    db.session.add(notification)
    db.session.commit()

    return {
        "status": "completed",
        "filename": filename
    }