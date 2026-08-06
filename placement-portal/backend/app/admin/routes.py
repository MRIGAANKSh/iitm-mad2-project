from flask import jsonify, request

from app.admin import admin_bp

from app.utils import role_required

from app.extensions import db

from app.models import (
    User,
    StudentProfile,
    CompanyProfile,
    PlacementDrive,
    Application
)
from flask_jwt_extended import jwt_required, get_jwt_identity

@admin_bp.route("/dashboard")
@role_required("admin")
def dashboard():

    total_students = StudentProfile.query.count()

    total_companies = CompanyProfile.query.count()

    total_drives = PlacementDrive.query.count()

    total_applications = Application.query.count()

    return jsonify({

        "students": total_students,

        "companies": total_companies,

        "drives": total_drives,

        "applications": total_applications

    }) 

@admin_bp.route("/companies/pending")
@role_required("admin")
def pending_companies():

    companies = CompanyProfile.query.filter_by(
        approval_status="pending"
    ).all()

    data = []

    for company in companies:

        data.append({

            "id": company.id,

            "company_name": company.company_name,

            "hr_name": company.hr_name,

            "website": company.website

        })

    return jsonify(data)


@admin_bp.route("/companies/<int:id>/approve", methods=["PUT"])
@role_required("admin")
def approve_company(id):

    company = CompanyProfile.query.get_or_404(id)

    company.approval_status = "approved"

    db.session.commit()

    return jsonify({
        "message": "Company approved."
    })


@admin_bp.route("/companies/<int:id>/reject", methods=["PUT"])
@role_required("admin")
def reject_company(id):

    company = CompanyProfile.query.get_or_404(id)

    company.approval_status = "rejected"

    db.session.commit()

    return jsonify({
        "message":"Company rejected."
    })


@admin_bp.route("/companies/<int:id>/blacklist", methods=["PUT"])
@role_required("admin")
def blacklist_company(id):

    company = CompanyProfile.query.get_or_404(id)

    company.is_blacklisted = True

    db.session.commit()

    return jsonify({

        "message":"Company blacklisted."

    })


@admin_bp.route("/students")
@role_required("admin")
def students():

    students = StudentProfile.query.all()

    data = []

    for student in students:

        user = User.query.get(student.user_id)

        data.append({

            "id": student.id,

            "name": user.name,

            "email": user.email,

            "branch": student.branch,

            "cgpa": student.cgpa,

            "placed": student.is_placed

        })

    return jsonify(data)


@admin_bp.route("/students/<int:id>/deactivate", methods=["PUT"])
@role_required("admin")
def deactivate_student(id):

    student = StudentProfile.query.get_or_404(id)

    user = User.query.get(student.user_id)

    user.is_active = False

    db.session.commit()

    return jsonify({

        "message":"Student deactivated."

    })

@admin_bp.route("/students/search")
@role_required("admin")
def search_students():

    keyword = request.args.get("q", "")

    students = StudentProfile.query.join(User).filter(

        User.name.ilike(f"%{keyword}%")

    ).all()

    data = []

    for student in students:

        user = User.query.get(student.user_id)

        data.append({

            "id": student.id,

            "name": user.name,

            "email": user.email,

            "branch": student.branch

        })

    return jsonify(data)


@admin_bp.route("/companies/search")
@role_required("admin")
def search_companies():

    keyword = request.args.get("q", "")

    companies = CompanyProfile.query.filter(

        CompanyProfile.company_name.ilike(
            f"%{keyword}%"
        )

    ).all()

    data = []

    for company in companies:

        data.append({

            "id": company.id,

            "company_name": company.company_name,

            "approval_status": company.approval_status

        })

    return jsonify(data)

@admin_bp.route("/companies")

def companies():

    companies = CompanyProfile.query.all()

    result = []

    for company in companies:

        user = User.query.get(company.user_id)

        result.append({

            "id": company.id,

            "company_name": company.company_name,

            "email": user.email,

            "hr_name": company.hr_name,

            "approval_status": company.approval_status,

            "is_active": user.is_active

        })

    return jsonify(result)


@admin_bp.route("/drives")
@jwt_required()
def get_all_drives():

    drives = PlacementDrive.query.all()

    result = []

    for drive in drives:

        company = CompanyProfile.query.get(drive.company_id)

        result.append({

            "id": drive.id,

            "company": company.company_name,

            "job_title": drive.job_title,

            "deadline": str(drive.application_deadline),

            "status": drive.status,

            "salary": drive.salary,

            "location": drive.location

        })

    return jsonify(result)


@admin_bp.route("/drives/<int:id>/approve", methods=["PUT"])
@jwt_required()
def approve_drive(id):

    drive = PlacementDrive.query.get_or_404(id)

    drive.status = "approved"

    db.session.commit()

    return jsonify({
        "message": "Drive Approved"
    })


@admin_bp.route("/drives/<int:id>/reject", methods=["PUT"])
@jwt_required()
def reject_drive(id):

    drive = PlacementDrive.query.get_or_404(id)

    drive.status = "rejected"

    db.session.commit()

    return jsonify({
        "message": "Drive Rejected"
    })


@admin_bp.route("/drives/<int:id>/close", methods=["PUT"])
@jwt_required()
def close_drive(id):

    drive = PlacementDrive.query.get_or_404(id)

    drive.status = "closed"

    db.session.commit()

    return jsonify({
        "message": "Drive Closed"
    })

