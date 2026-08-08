from datetime import datetime
from flask_mail import Message

from app.extensions import mail
from app.celery_app import celery
from app.extensions import db

from app.models import (
    PlacementDrive,
    Application,
    StudentProfile,
    User
)

import os


@celery.task
def generate_monthly_report():

    now = datetime.now()

    month = now.month
    year = now.year

    # =====================================================
    # COUNT PLACEMENT DRIVES
    # =====================================================

    drives_count = PlacementDrive.query.filter(
        db.extract(
            "month",
            PlacementDrive.created_at
        ) == month,

        db.extract(
            "year",
            PlacementDrive.created_at
        ) == year
    ).count()

    # =====================================================
    # COUNT APPLICATIONS
    # =====================================================

    applications_count = Application.query.filter(
        db.extract(
            "month",
            Application.applied_at
        ) == month,

        db.extract(
            "year",
            Application.applied_at
        ) == year
    ).count()

    # =====================================================
    # COUNT SELECTED STUDENTS
    # =====================================================

    selected_count = Application.query.filter(
        Application.status == "selected",

        db.extract(
            "month",
            Application.applied_at
        ) == month,

        db.extract(
            "year",
            Application.applied_at
        ) == year
    ).count()

    # =====================================================
    # COUNT STUDENTS
    # =====================================================

    students_count = StudentProfile.query.count()

    # =====================================================
    # CREATE REPORT FOLDER
    # =====================================================

    report_folder = "reports"

    os.makedirs(
        report_folder,
        exist_ok=True
    )

    # =====================================================
    # REPORT FILE
    # =====================================================

    filename = (
        f"monthly_report_"
        f"{year}_{month:02d}.html"
    )

    filepath = os.path.join(
        report_folder,
        filename
    )

    # =====================================================
    # HTML REPORT
    # =====================================================

    html = f"""
<!DOCTYPE html>

<html>

<head>

    <meta charset="UTF-8">

    <title>
        Monthly Placement Report
    </title>

    <style>

        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
        }}

        h1 {{
            color: #333;
        }}

        .card {{
            border: 1px solid #ddd;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
        }}

        .value {{
            font-size: 28px;
            font-weight: bold;
        }}

    </style>

</head>

<body>

    <h1>
        Monthly Placement Activity Report
    </h1>

    <p>
        Report Period:
        {month:02d}/{year}
    </p>

    <div class="card">

        <h3>
            Total Placement Drives
        </h3>

        <div class="value">
            {drives_count}
        </div>

    </div>

    <div class="card">

        <h3>
            Total Applications
        </h3>

        <div class="value">
            {applications_count}
        </div>

    </div>

    <div class="card">

        <h3>
            Students Selected
        </h3>

        <div class="value">
            {selected_count}
        </div>

    </div>

    <div class="card">

        <h3>
            Total Registered Students
        </h3>

        <div class="value">
            {students_count}
        </div>

    </div>

</body>

</html>
"""

    # =====================================================
    # SAVE REPORT
    # =====================================================

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(html)

    # =====================================================
    # SEND REPORT TO ADMIN
    # =====================================================

    admin = User.query.filter_by(
        role="admin"
    ).first()

    if admin:

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            html_content = file.read()

        message = Message(

            subject="Monthly Placement Activity Report",

            recipients=[
                admin.email
            ],

            html=html_content

        )

        mail.send(message)

    # =====================================================
    # RETURN RESULT
    # =====================================================

    return {

        "status": "completed",

        "report": filepath,

        "drives": drives_count,

        "applications": applications_count,

        "selected": selected_count

    }