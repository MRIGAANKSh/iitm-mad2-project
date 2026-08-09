from flask import jsonify, request

from app.admin import admin_bp
from app.extensions import cache
from app.utils import role_required

from app.extensions import db

from app.models import (
    User,
    StudentProfile,
    CompanyProfile,
    PlacementDrive,
    Application
)

from flask_jwt_extended import jwt_required, get_jwt_identity,get_jwt



def admin_required():

    claims = get_jwt()

    if claims.get("role") != "admin":

        return False

    return True

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
    cache.delete("approved_drives")
    return jsonify({
        "message": "Drive Approved"
    })


@admin_bp.route("/drives/<int:id>/reject", methods=["PUT"])
@jwt_required()
def reject_drive(id):

    drive = PlacementDrive.query.get_or_404(id)

    drive.status = "rejected"
    
    db.session.commit()
    cache.delete("approved_drives")
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

@admin_bp.route("/students/search")
@jwt_required()
def search_students():

    if not admin_required():

        return jsonify({
            "message": "Admin access required."
        }), 403

    query = request.args.get(
        "q",
        ""
    ).strip()

    students = StudentProfile.query.join(
        User,
        StudentProfile.user_id == User.id
    ).filter(
        db.or_(
            User.name.ilike(f"%{query}%"),
            User.email.ilike(f"%{query}%"),
            StudentProfile.student_id.ilike(f"%{query}%"),
            StudentProfile.branch.ilike(f"%{query}%")
        )
    ).all()

    result = []

    for student in students:

        user = User.query.get(
            student.user_id
        )

        result.append({

            "id": student.id,

            "student_id": student.student_id,

            "name": user.name,

            "email": user.email,

            "phone": student.phone,

            "branch": student.branch,

            "cgpa": student.cgpa,

            "graduation_year":
                student.graduation_year,

            "is_active":
                user.is_active

        })

    return jsonify(result)


@admin_bp.route("/companies/search")
@jwt_required()
def search_companies():

    if not admin_required():

        return jsonify({
            "message": "Admin access required."
        }), 403

    query = request.args.get(
        "q",
        ""
    ).strip()

    companies = CompanyProfile.query.join(
        User,
        CompanyProfile.user_id == User.id
    ).filter(
        db.or_(
            CompanyProfile.company_name.ilike(
                f"%{query}%"
            ),

            User.email.ilike(
                f"%{query}%"
            ),

            CompanyProfile.hr_name.ilike(
                f"%{query}%"
            )
        )
    ).all()

    result = []

    for company in companies:

        user = User.query.get(
            company.user_id
        )

        result.append({

            "id": company.id,

            "company_name":
                company.company_name,

            "email":
                user.email,

            "hr_name":
                company.hr_name,

            "hr_email":
                company.hr_email,

            "approval_status":
                company.approval_status,

            "is_blacklisted":
                company.is_blacklisted,

            "is_active":
                user.is_active

        })

    return jsonify(result)


@admin_bp.route(
    "/students/<int:id>/deactivate",
    methods=["PUT"]
)
@jwt_required()
def deactivate_student(id):

    if not admin_required():
        return jsonify({
            "message": "Admin access required."
        }), 403

    student = StudentProfile.query.get_or_404(id)

    user = User.query.get_or_404(
        student.user_id
    )

    user.is_active = False

    db.session.commit()

    return jsonify({
        "message": "Student deactivated successfully."
    })


@admin_bp.route(
    "/students/<int:id>/activate",
    methods=["PUT"]
)
@jwt_required()
def activate_student(id):

    if not admin_required():
        return jsonify({
            "message": "Admin access required."
        }), 403

    student = StudentProfile.query.get_or_404(id)

    user = User.query.get_or_404(
        student.user_id
    )

    user.is_active = True

    db.session.commit()

    return jsonify({
        "message": "Student activated successfully."
    })

@admin_bp.route(
    "/companies/<int:id>/blacklist",
    methods=["PUT"]
)
@jwt_required()
def blacklist_company(id):

    if not admin_required():
        return jsonify({
            "message": "Admin access required."
        }), 403

    company = CompanyProfile.query.get_or_404(id)

    company.is_blacklisted = True
    company.approval_status = "rejected"

    db.session.commit()

    return jsonify({
        "message": "Company blacklisted successfully."
    }), 200


@admin_bp.route(
    "/companies/<int:id>/unblacklist",
    methods=["PUT"]
)
@jwt_required()
def unblacklist_company(id):

    if not admin_required():
        return jsonify({
            "message": "Admin access required."
        }), 403

    company = CompanyProfile.query.get_or_404(id)

    company.is_blacklisted = False
    company.approval_status = "approved"

    db.session.commit()

    return jsonify({
        "message": "Company removed from blacklist and approved again."
    }), 200


@admin_bp.route(
    "/companies/<int:id>/deactivate",
    methods=["PUT"]
)


@jwt_required()
def deactivate_company(id):

    if not admin_required():

        return jsonify({
            "message": "Admin access required."
        }), 403

    company = CompanyProfile.query.get_or_404(id)

    user = User.query.get_or_404(
        company.user_id
    )

    user.is_active = False

    db.session.commit()

    return jsonify({

        "message":
            "Company deactivated successfully."

    })

@admin_bp.route(
    "/companies/<int:id>/activate",
    methods=["PUT"]
)
@jwt_required()
def activate_company(id):

    if not admin_required():

        return jsonify({
            "message": "Admin access required."
        }), 403

    company = CompanyProfile.query.get_or_404(id)

    user = User.query.get_or_404(
        company.user_id
    )

    user.is_active = True

    db.session.commit()

    return jsonify({

        "message":
            "Company activated successfully."

    })


@admin_bp.route("/applications")
@jwt_required()
def applications():

    claims = get_jwt()

    if claims.get("role") != "admin":

        return jsonify({
            "message": "Admin access required."
        }), 403

    applications = Application.query.order_by(
        Application.applied_at.desc()
    ).all()

    result = []

    for application in applications:

        student = StudentProfile.query.get(
            application.student_id
        )

        drive = PlacementDrive.query.get(
            application.drive_id
        )

        if not student or not drive:
            continue

        user = User.query.get(
            student.user_id
        )

        company = CompanyProfile.query.get(
            drive.company_id
        )

        result.append({

            "id": application.id,

            "student_name":
                user.name if user else "",

            "student_email":
                user.email if user else "",

            "student_id":
                student.student_id,

            "branch":
                student.branch,

            "cgpa":
                student.cgpa,

            "company":
                company.company_name
                if company else "",

            "job_title":
                drive.job_title,

            "status":
                application.status,

            "applied_at":
                application.applied_at.isoformat()
                if application.applied_at
                else None

        })

    return jsonify(result)


@admin_bp.route("/applications/stats")
@jwt_required()
def application_stats():

    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({
            "message": "Admin access required."
        }), 403

    return jsonify({

        "total": Application.query.count(),

        "applied": Application.query.filter_by(
            status="applied"
        ).count(),

        "shortlisted": Application.query.filter_by(
            status="shortlisted"
        ).count(),

        "selected": Application.query.filter_by(
            status="selected"
        ).count(),

        "rejected": Application.query.filter_by(
            status="rejected"
        ).count()

    })