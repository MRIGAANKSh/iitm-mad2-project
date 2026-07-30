from flask import jsonify, request

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
            "message":"Company not approved."
        }),403

    data = request.get_json()

    drive = PlacementDrive(

        company_id=company.id,

        job_title=data["job_title"],

        job_description=data["job_description"],

        eligibility_branch=data["eligibility_branch"],

        minimum_cgpa=data["minimum_cgpa"],

        graduation_year=data["graduation_year"],

        application_deadline=data["application_deadline"],

        salary=data.get("salary"),

        location=data.get("location"),

        employment_type=data.get("employment_type"),

        vacancies=data.get("vacancies")
    )

    db.session.add(drive)

    db.session.commit()

    return jsonify({
        "message":"Drive created successfully."
    }),201

@company_bp.route("/drives")
@jwt_required()
def company_drives():

    user_id = get_jwt_identity()

    company = CompanyProfile.query.filter_by(
        user_id=user_id
    ).first()

    drives = PlacementDrive.query.filter_by(
        company_id=company.id
    ).all()

    result = []

    for drive in drives:

        applicants = Application.query.filter_by(
            drive_id=drive.id
        ).count()

        result.append({

            "id":drive.id,

            "job_title":drive.job_title,

            "status":drive.status,

            "deadline":str(drive.application_deadline),

            "applicants":applicants

        })

    return jsonify(result)


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

