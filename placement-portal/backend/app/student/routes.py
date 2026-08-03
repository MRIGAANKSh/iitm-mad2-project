from flask import jsonify, request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from datetime import date

from app.student import student_bp
from app.extensions import db
from app.utils import role_required

from app.models import (
    User,
    StudentProfile,
    CompanyProfile,
    PlacementDrive,
    Application
)

@student_bp.route("/dashboard")
@jwt_required()
@role_required("student")
def dashboard():

    user_id = get_jwt_identity()

    student = StudentProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()

    drives = PlacementDrive.query.filter_by(
        status="approved"
    ).all()

    data = []

    for drive in drives:

        company = CompanyProfile.query.get(
            drive.company_id
        )

        data.append({

            "id": drive.id,

            "company": company.company_name,

            "job_title": drive.job_title,

            "deadline": str(
                drive.application_deadline
            ),

            "minimum_cgpa": drive.minimum_cgpa,

            "branch": drive.eligibility_branch

        })

    return jsonify({

        "student": student.student_id,

        "available_drives": data

    })

@student_bp.route("/drives/search")
@jwt_required()
@role_required("student")
def search():

    keyword = request.args.get("q", "")

    drives = PlacementDrive.query.filter(

        PlacementDrive.status == "approved",

        PlacementDrive.job_title.ilike(
            f"%{keyword}%"
        )

    ).all()

    result = []

    for drive in drives:

        company = CompanyProfile.query.get(
            drive.company_id
        )

        result.append({

            "id": drive.id,

            "company": company.company_name,

            "job_title": drive.job_title

        })

    return jsonify(result)

@student_bp.route(
    "/drives/<int:id>/apply",
    methods=["POST"]
)
@jwt_required()
@role_required("student")
def apply(id):

    user_id = get_jwt_identity()

    student = StudentProfile.query.filter_by(
        user_id=user_id
    ).first()

    drive = PlacementDrive.query.get_or_404(id)

    if drive.status != "approved":

        return jsonify({
            "message":"Drive not approved."
        }),400

    if drive.application_deadline < date.today():

        return jsonify({
            "message":"Deadline passed."
        }),400

    if student.cgpa < drive.minimum_cgpa:

        return jsonify({
            "message":"CGPA not eligible."
        }),400

    if student.branch != drive.eligibility_branch:

        return jsonify({
            "message":"Branch not eligible."
        }),400

    already = Application.query.filter_by(

        student_id=student.id,

        drive_id=id

    ).first()

    if already:

        return jsonify({

            "message":"Already applied."

        }),400

    application = Application(

        student_id=student.id,

        drive_id=id

    )

    db.session.add(application)

    db.session.commit()

    return jsonify({

        "message":"Application submitted."

    }),201


@student_bp.route("/applications")
@jwt_required()
@role_required("student")
def applications():

    user_id = get_jwt_identity()

    student = StudentProfile.query.filter_by(
        user_id=user_id
    ).first()

    apps = Application.query.filter_by(
        student_id=student.id
    ).all()

    result = []

    for app in apps:

        drive = PlacementDrive.query.get(
            app.drive_id
        )

        company = CompanyProfile.query.get(
            drive.company_id
        )

        result.append({

            "company": company.company_name,

            "job_title": drive.job_title,

            "status": app.status,

            "applied_at": str(
                app.applied_at
            )

        })

    return jsonify(result)

@student_bp.route("/history")
@jwt_required()
@role_required("student")
def history():

    user_id = get_jwt_identity()

    student = StudentProfile.query.filter_by(
        user_id=user_id
    ).first()

    apps = Application.query.filter(

        Application.student_id == student.id,

        Application.status == "selected"

    ).all()

    data = []

    for app in apps:

        drive = PlacementDrive.query.get(
            app.drive_id
        )

        company = CompanyProfile.query.get(
            drive.company_id
        )

        data.append({

            "company": company.company_name,

            "job_title": drive.job_title,

            "selected_on": str(
                app.applied_at
            )

        })

    return jsonify(data)

@student_bp.route(
    "/profile",
    methods=["PUT"]
)
@jwt_required()
@role_required("student")
def update_profile():

    user_id = get_jwt_identity()

    student = StudentProfile.query.filter_by(
        user_id=user_id
    ).first()

    data = request.get_json()

    student.phone = data.get(
        "phone",
        student.phone
    )

    student.cgpa = data.get(
        "cgpa",
        student.cgpa
    )

    student.branch = data.get(
        "branch",
        student.branch
    )

    db.session.commit()

    return jsonify({

        "message":"Profile updated."

    })




@student_bp.route("/drives", methods=["GET"])
@jwt_required()
def get_drives():

    user_id = get_jwt_identity()

    student = StudentProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()

    drives = PlacementDrive.query.filter_by(
        status="approved"
    ).all()

    result = []

    for drive in drives:

        company = CompanyProfile.query.get(drive.company_id)

        applied = Application.query.filter_by(
            student_id=student.id,
            drive_id=drive.id
        ).first()

        result.append({

            "id": drive.id,

            "company": company.company_name,

            "job_title": drive.job_title,

            "branch": drive.eligibility_branch,

            "cgpa": drive.minimum_cgpa,

            "deadline": str(drive.application_deadline),

            "already_applied": applied is not None

        })

    return jsonify(result)


