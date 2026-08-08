
from flask import jsonify, request
from datetime import datetime

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)

from app.company import company_bp
from app.extensions import db

from app.models import (
    User,
    CompanyProfile,
    PlacementDrive,
    Application,
    Interview,
    StudentProfile
)


# =========================================================
# COMPANY DASHBOARD
# =========================================================

@company_bp.route("/dashboard")
@jwt_required()
def dashboard():

    user_id = get_jwt_identity()

    company = CompanyProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()

    drives = PlacementDrive.query.filter_by(
        company_id=company.id
    ).all()

    total_applicants = 0

    for drive in drives:

        total_applicants += Application.query.filter_by(
            drive_id=drive.id
        ).count()

    return jsonify({

        "company_name": company.company_name,

        "approval_status": company.approval_status,

        "total_drives": len(drives),

        "total_applicants": total_applicants

    })
@company_bp.route("/applications", methods=["GET"])
@jwt_required()
def company_applications():

    user_id = get_jwt_identity()

    # Get logged-in company
    company = CompanyProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()

    # Get all drives belonging to this company
    drives = PlacementDrive.query.filter_by(
        company_id=company.id
    ).all()

    drive_ids = [drive.id for drive in drives]

    # No drives
    if not drive_ids:
        return jsonify([]), 200

    # Get applications for company's drives
    applications = Application.query.filter(
        Application.drive_id.in_(drive_ids)
    ).all()

    data = []

    for app in applications:

        student = StudentProfile.query.get(app.student_id)

        if not student:
            continue

        user = User.query.get(student.user_id)

        if not user:
            continue

        drive = PlacementDrive.query.get(app.drive_id)

        data.append({
            "application_id": app.id,
            "drive_id": drive.id,
            "job_title": drive.job_title,
            "student_name": user.name,
            "email": user.email,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "status": app.status
        })

    return jsonify(data), 200

# =========================================================
# CREATE DRIVE
# =========================================================

@company_bp.route("/drives", methods=["POST"])
@jwt_required()
def create_drive():

    user_id = get_jwt_identity()

    company = CompanyProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()

    if company.approval_status != "approved":

        return jsonify({
            "message": "Company not approved."
        }), 403

    data = request.get_json()

    if not data:

        return jsonify({
            "message": "No JSON data received."
        }), 400

    print("Received Data:", data)

    required_fields = [

        "job_title",
        "job_description",
        "eligibility_branch",
        "minimum_cgpa",
        "graduation_year",
        "application_deadline"

    ]

    missing_fields = []

    for field in required_fields:

        if field not in data or data[field] in [None, ""]:

            missing_fields.append(field)

    if missing_fields:

        return jsonify({

            "message": "Missing required fields.",

            "missing_fields": missing_fields

        }), 400


    # Convert deadline to date
    try:

        application_deadline = datetime.strptime(
            data["application_deadline"],
            "%Y-%m-%d"
        ).date()

    except (ValueError, KeyError):

        return jsonify({

            "message":
            "Invalid application deadline. Use YYYY-MM-DD."

        }), 400


    try:

        drive = PlacementDrive(

            company_id=company.id,

            job_title=data.get("job_title"),

            job_description=data.get(
                "job_description"
            ),

            eligibility_branch=data.get(
                "eligibility_branch"
            ),

            minimum_cgpa=float(
                data.get("minimum_cgpa")
            ),

            graduation_year=int(
                data.get("graduation_year")
            ),

            application_deadline=application_deadline,

            salary=(
                float(data.get("salary"))
                if data.get("salary")
                else None
            ),

            location=data.get("location"),

            employment_type=data.get(
                "employment_type"
            ),

            vacancies=(
                int(data.get("vacancies"))
                if data.get("vacancies")
                else None
            )
        )

        db.session.add(drive)

        db.session.commit()

    except (ValueError, TypeError) as e:

        db.session.rollback()

        return jsonify({

            "message":
            "Invalid numeric value provided.",

            "error": str(e)

        }), 400


    return jsonify({

        "message":
        "Drive created successfully.",

        "drive_id": drive.id

    }), 201


# =========================================================
# GET COMPANY DRIVES
# =========================================================

@company_bp.route("/drives", methods=["GET"])
@jwt_required()
def company_drives():

    user_id = get_jwt_identity()

    company = CompanyProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()

    drives = PlacementDrive.query.filter_by(
        company_id=company.id
    ).all()

    result = []

    for drive in drives:

        applicants = Application.query.filter_by(
            drive_id=drive.id
        ).count()

        result.append({

            "id": drive.id,

            "job_title": drive.job_title,

            "deadline": str(
                drive.application_deadline
            ),

            "status": drive.status,

            "applicants": applicants

        })

    return jsonify(result), 200


@company_bp.route("/applications", methods=["GET"])
@jwt_required()
def all_applicants():

    user_id = get_jwt_identity()

    # Get logged-in company
    company = CompanyProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()

    # Get all drives belonging to this company
    drives = PlacementDrive.query.filter_by(
        company_id=company.id
    ).all()

    data = []

    for drive in drives:

        # Get applications for this drive
        applications = Application.query.filter_by(
            drive_id=drive.id
        ).all()

        for app in applications:

            student = StudentProfile.query.get(app.student_id)

            if not student:
                continue

            user = User.query.get(student.user_id)

            if not user:
                continue

            data.append({

                "application_id": app.id,

                "student_name": user.name,

                "email": user.email,

                "job_title": drive.job_title,

                "drive_id": drive.id,

                "branch": student.branch,

                "cgpa": student.cgpa,

                "resume": student.resume,

                "status": app.status

            })

    return jsonify(data), 200

# =========================================================
# GET APPLICANTS FOR A SPECIFIC DRIVE
# =========================================================
# =========================================================
# GET APPLICANTS FOR A SPECIFIC DRIVE
# =========================================================

@company_bp.route(
    "/drives/<int:drive_id>/applicants",
    methods=["GET"]
)
@jwt_required()
def drive_applicants(drive_id):

    user_id = get_jwt_identity()

    # Get logged-in company
    company = CompanyProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()


    # Make sure the drive belongs to this company
    drive = PlacementDrive.query.filter_by(
        id=drive_id,
        company_id=company.id
    ).first()


    if not drive:

        return jsonify({
            "message": "Drive not found or does not belong to this company."
        }), 404


    # Get applications ONLY for this drive
    applications = Application.query.filter_by(
        drive_id=drive.id
    ).all()


    data = []


    for app in applications:

        # Get student profile
        student = StudentProfile.query.get(
            app.student_id
        )


        if not student:
            continue


        # Get user
        user = User.query.get(
            student.user_id
        )


        if not user:
            continue


        data.append({

            "application_id": app.id,

            "drive_id": drive.id,

            "job_title": drive.job_title,

            "student_name": user.name,

            "email": user.email,

            "branch": student.branch,

            "cgpa": student.cgpa,

            "resume": student.resume,

            "status": app.status

        })


    return jsonify(data), 200

# =========================================================
# UPDATE APPLICATION STATUS
# =========================================================

@company_bp.route(
    "/applications/<int:id>/status",
    methods=["PUT"]
)
@jwt_required()
def update_status(id):

    user_id = get_jwt_identity()

    company = CompanyProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()


    application = Application.query.get_or_404(id)

    # Get drive connected to application
    drive = PlacementDrive.query.filter_by(
        id=application.drive_id,
        company_id=company.id
    ).first()

    if not drive:

        return jsonify({

            "message":
            "You are not authorized to update this application."

        }), 403


    data = request.get_json()

    if not data or not data.get("status"):

        return jsonify({

            "message":
            "Status is required."

        }), 400


    allowed_statuses = [

        "Applied",
        "Shortlisted",
        "Rejected",
        "Selected"

    ]

    status = data.get("status")

    if status not in allowed_statuses:

        return jsonify({

            "message":
            "Invalid application status."

        }), 400


    application.status = status

    db.session.commit()


    return jsonify({

        "message":
        "Status updated successfully."

    }), 200


# =========================================================
# SCHEDULE INTERVIEW
# =========================================================

@company_bp.route(
    "/applications/<int:id>/interview",
    methods=["POST"]
)
@jwt_required()
def schedule_interview(id):

    user_id = get_jwt_identity()

    company = CompanyProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()

    application = Application.query.get_or_404(id)

    drive = PlacementDrive.query.filter_by(
        id=application.drive_id,
        company_id=company.id
    ).first()

    if not drive:

        return jsonify({

            "message":
            "You are not authorized to schedule this interview."

        }), 403


    data = request.get_json()

    if not data:

        return jsonify({

            "message":
            "No JSON data received."

        }), 400


    interview = Interview(

        application_id=id,

        interview_date=data.get(
            "interview_date"
        ),

        interview_type=data.get(
            "interview_type"
        ),

        status="Scheduled",

        remarks=data.get(
            "remarks"
        )

    )

    db.session.add(interview)

    db.session.commit()


    return jsonify({

        "message":
        "Interview scheduled."

    }), 201


# =========================================================
# GET SINGLE DRIVE
# =========================================================

@company_bp.route(
    "/drives/<int:id>",
    methods=["GET"]
)
@jwt_required()
def get_drive(id):

    user_id = get_jwt_identity()

    company = CompanyProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()

    drive = PlacementDrive.query.filter_by(
        id=id,
        company_id=company.id
    ).first_or_404()


    return jsonify({

        "id": drive.id,

        "job_title": drive.job_title,

        "job_description":
        drive.job_description,

        "eligibility_branch":
        drive.eligibility_branch,

        "minimum_cgpa":
        drive.minimum_cgpa,

        "graduation_year":
        drive.graduation_year,

        "application_deadline":
        str(drive.application_deadline),

        "salary":
        drive.salary,

        "location":
        drive.location,

        "employment_type":
        drive.employment_type,

        "vacancies":
        drive.vacancies

    }), 200


# =========================================================
# CLOSE DRIVE
# =========================================================

@company_bp.route(
    "/drives/<int:id>/close",
    methods=["PUT"]
)
@jwt_required()
def close_drive(id):

    user_id = get_jwt_identity()

    company = CompanyProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()

    drive = PlacementDrive.query.filter_by(
        id=id,
        company_id=company.id
    ).first_or_404()


    drive.status = "closed"

    db.session.commit()


    return jsonify({

        "message":
        "Drive closed successfully."

    }), 200


# =========================================================
# DELETE DRIVE
# =========================================================

@company_bp.route(
    "/drives/<int:id>",
    methods=["DELETE"]
)
@jwt_required()
def delete_drive(id):

    user_id = get_jwt_identity()

    company = CompanyProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()

    drive = PlacementDrive.query.filter_by(
        id=id,
        company_id=company.id
    ).first_or_404()


    applications = Application.query.filter_by(
        drive_id=id
    ).count()


    if applications > 0:

        return jsonify({

            "message":
            "Cannot delete a drive with applications."

        }), 400


    db.session.delete(drive)

    db.session.commit()


    return jsonify({

        "message":
        "Drive deleted successfully."

    }), 200


# =========================================================
# EDIT DRIVE
# =========================================================

@company_bp.route(
    "/drives/<int:id>",
    methods=["PUT"]
)
@jwt_required()
def edit_drive(id):

    user_id = get_jwt_identity()

    company = CompanyProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()


    drive = PlacementDrive.query.filter_by(
        id=id,
        company_id=company.id
    ).first_or_404()


    data = request.get_json()

    if not data:

        return jsonify({

            "message":
            "No JSON data received."

        }), 400


    drive.job_title = data.get(
        "job_title",
        drive.job_title
    )

    drive.job_description = data.get(
        "job_description",
        drive.job_description
    )

    drive.eligibility_branch = data.get(
        "eligibility_branch",
        drive.eligibility_branch
    )


    try:

        if data.get("minimum_cgpa") is not None:

            drive.minimum_cgpa = float(
                data.get("minimum_cgpa")
            )


        if data.get("graduation_year") is not None:

            drive.graduation_year = int(
                data.get("graduation_year")
            )


        if data.get("application_deadline"):

            drive.application_deadline = datetime.strptime(
                data["application_deadline"],
                "%Y-%m-%d"
            ).date()


        if "salary" in data:

            drive.salary = (
                float(data["salary"])
                if data["salary"] not in [None, ""]
                else None
            )


        drive.location = data.get(
            "location",
            drive.location
        )

        drive.employment_type = data.get(
            "employment_type",
            drive.employment_type
        )


        if "vacancies" in data:

            drive.vacancies = (
                int(data["vacancies"])
                if data["vacancies"] not in [None, ""]
                else None
            )


    except (ValueError, TypeError):

        db.session.rollback()

        return jsonify({

            "message":
            "Invalid numeric or date value."

        }), 400


    db.session.commit()


    return jsonify({

        "message":
        "Drive updated successfully."

    }), 200

