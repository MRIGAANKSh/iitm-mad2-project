from flask import jsonify, request
import os

from werkzeug.utils import secure_filename

from flask import current_app
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
def dashboard():

    user_id = get_jwt_identity()

    student = StudentProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()

    applications = Application.query.filter_by(
        student_id=student.id
    ).count()

    selected = Application.query.filter_by(
        student_id=student.id,
        status="Selected"
    ).count()

    shortlisted = Application.query.filter_by(
        student_id=student.id,
        status="Shortlisted"
    ).count()

    drives = PlacementDrive.query.filter_by(
        status="approved"
    ).count()

    return jsonify({

        "applications": applications,

        "selected": selected,

        "shortlisted": shortlisted,

        "drives": drives

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
def applications():

    user_id = get_jwt_identity()

    student = StudentProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()

    apps = Application.query.filter_by(
        student_id=student.id
    ).all()

    result = []

    for app in apps:

        drive = PlacementDrive.query.get(
            app.drive_id
        )

        if not drive:
            continue

        company = CompanyProfile.query.get(
            drive.company_id
        )

        if not company:
            continue

        result.append({

            "company": company.company_name,

            "job_title": drive.job_title,

            "status": app.status,

            # FIX: use applied_at
            "date": str(app.applied_at)

        })

    return jsonify(result), 200
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


@student_bp.route("/profile", methods=["GET"])
@jwt_required()
@role_required("student")
def get_profile():

    user_id = get_jwt_identity()

    student = StudentProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()

    user = User.query.get(student.user_id)

    if not user:
        return jsonify({
            "message": "User not found."
        }), 404

    return jsonify({

        "name": user.name,

        "email": user.email,

        "phone": student.phone,

        "branch": student.branch,

        "cgpa": student.cgpa,

        "resume": student.resume

    }), 200



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

@student_bp.route("/drives")
@jwt_required()
def approved_drives():

    user_id = get_jwt_identity()

    student = StudentProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()

    search = request.args.get("search", "")
    branch = request.args.get("branch", "")
    min_cgpa = request.args.get("min_cgpa", type=float)

    query = PlacementDrive.query.filter_by(
        status="approved"
    )

    # Search by job title
    if search:
        query = query.filter(
            PlacementDrive.job_title.ilike(
                f"%{search}%"
            )
        )

    # Branch filtering
    if branch:
        query = query.filter(
            PlacementDrive.eligibility_branch.ilike(
                f"%{branch}%"
            )
        )

    # CGPA filtering
    if min_cgpa is not None:
        query = query.filter(
            PlacementDrive.minimum_cgpa <= min_cgpa
        )

    drives = query.all()

    data = []

    for drive in drives:

        company = CompanyProfile.query.get(
            drive.company_id
        )

        applied = Application.query.filter_by(
            drive_id=drive.id,
            student_id=student.id
        ).first()

        data.append({

            "id": drive.id,

            "company": company.company_name,

            "job_title": drive.job_title,

            "job_description": drive.job_description,

            "eligibility_branch":
                drive.eligibility_branch,

            "minimum_cgpa":
                drive.minimum_cgpa,

            "graduation_year":
                drive.graduation_year,

            "deadline":
                str(drive.application_deadline),

            "salary":
                drive.salary,

            "location":
                drive.location,

            "employment_type":
                drive.employment_type,

            "vacancies":
                drive.vacancies,

            "already_applied":
                applied is not None

        })

    return jsonify(data)

@student_bp.route(
    "/upload-resume",
    methods=["POST"]
)
@jwt_required()
def upload_resume():

    user_id = get_jwt_identity()

    student = StudentProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()

    if "resume" not in request.files:
        return jsonify({
            "message": "No file selected."
        }), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({
            "message": "Invalid file."
        }), 400

    upload_folder = current_app.config[
        "UPLOAD_FOLDER"
    ]

    # Make sure uploads directory exists
    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    filename = secure_filename(
        file.filename
    )

    filepath = os.path.join(
        upload_folder,
        filename
    )

    file.save(filepath)

    student.resume = filename

    db.session.commit()

    return jsonify({
        "message":
            "Resume uploaded successfully.",
        "filename":
            filename
    }), 200




@student_bp.route("/resume")
@jwt_required()
def get_resume():

    user_id = get_jwt_identity()

    student = StudentProfile.query.filter_by(
        user_id=user_id
    ).first_or_404()

    return jsonify({

        "resume":student.resume

    })