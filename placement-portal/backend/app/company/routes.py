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

    # Convert date string to Python date object
    try:
        application_deadline = datetime.strptime(
        data["application_deadline"],
        "%Y-%m-%d"
    ).date()
    except (ValueError, KeyError):
        return jsonify({
        "message": "Invalid application deadline. Use YYYY-MM-DD."
    }), 400

    drive = PlacementDrive(
    company_id=company.id,
    job_title=data.get("job_title"),
    job_description=data.get("job_description"),
    eligibility_branch=data.get("eligibility_branch"),
    minimum_cgpa=float(data.get("minimum_cgpa")),
    graduation_year=int(data.get("graduation_year")),
    application_deadline=application_deadline,
    salary=float(data.get("salary")) if data.get("salary") else None,
    location=data.get("location"),
    employment_type=data.get("employment_type"),
    vacancies=int(data.get("vacancies")) if data.get("vacancies") else None
)
    db.session.add(drive)
    db.session.commit()

    return jsonify({
        "message": "Drive created successfully.",
        "drive_id": drive.id
    }), 201

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
            "deadline": str(drive.application_deadline),
            "status": drive.status,
            "applicants": applicants
        })

    return jsonify(result), 200

@company_bp.route("/drives/<int:id>/applications")
@jwt_required()
def applicants(id):

    applications = Application.query.filter_by(
        drive_id=id
    ).all()

    data=[]

    for app in applications:

        student = StudentProfile.query.get(app.student_id)

        user = User.query.get(student.user_id)

        data.append({

            "application_id":app.id,

            "student_name":user.name,

            "email":user.email,

            "branch":student.branch,

            "cgpa":student.cgpa,

            "status":app.status

        })

    return jsonify(data)

@company_bp.route(
    "/applications/<int:id>/status",
    methods=["PUT"]
)
@jwt_required()
def update_status(id):

    application = Application.query.get_or_404(id)

    data = request.get_json()

    application.status = data["status"]

    db.session.commit()

    return jsonify({

        "message":"Status updated."

    })

@company_bp.route(
    "/applications/<int:id>/interview",
    methods=["POST"]
)
@jwt_required()
def schedule_interview(id):

    application = Application.query.get_or_404(id)

    data = request.get_json()

    interview = Interview(

        application_id=id,

        interview_date=data["interview_date"],

        interview_type=data["interview_type"],

        status="Scheduled",

        remarks=data.get("remarks")

    )

    db.session.add(interview)

    db.session.commit()

    return jsonify({

        "message":"Interview scheduled."

    })

@company_bp.route("/drives/<int:id>", methods=["GET"])
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
        "job_description": drive.job_description,
        "eligibility_branch": drive.eligibility_branch,
        "minimum_cgpa": drive.minimum_cgpa,
        "graduation_year": drive.graduation_year,
        "application_deadline": str(drive.application_deadline),
        "salary": drive.salary,
        "location": drive.location,
        "employment_type": drive.employment_type,
        "vacancies": drive.vacancies
    })

@company_bp.route("/drives/<int:id>/close", methods=["PUT"])
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
        "message": "Drive closed successfully."
    })


@company_bp.route("/drives/<int:id>", methods=["DELETE"])
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
            "message": "Cannot delete a drive with applications."
        }), 400

    db.session.delete(drive)
    db.session.commit()

    return jsonify({
        "message": "Drive deleted successfully."
    })

@company_bp.route("/drives/<int:id>", methods=["PUT"])
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
            "message": "No JSON data received."
        }), 400

    drive.job_title = data.get("job_title", drive.job_title)
    drive.job_description = data.get("job_description", drive.job_description)
    drive.eligibility_branch = data.get("eligibility_branch", drive.eligibility_branch)
    drive.minimum_cgpa = float(data.get("minimum_cgpa", drive.minimum_cgpa))
    drive.graduation_year = int(data.get("graduation_year", drive.graduation_year))

    if data.get("application_deadline"):
        try:
            drive.application_deadline = datetime.strptime(
                data["application_deadline"],
                "%Y-%m-%d"
            ).date()
        except ValueError:
            return jsonify({
                "message": "Invalid application deadline. Use YYYY-MM-DD."
            }), 400

    drive.salary = float(data.get("salary")) if data.get("salary") else drive.salary
    drive.location = data.get("location", drive.location)
    drive.employment_type = data.get("employment_type", drive.employment_type)
    drive.vacancies = int(data.get("vacancies")) if data.get("vacancies") else drive.vacancies

    db.session.commit()

    return jsonify({
        "message": "Drive updated successfully."
    }), 200