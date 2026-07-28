from flask import request, jsonify

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_jwt_extended import (
    create_access_token
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from app.auth import auth_bp

from app.extensions import db

from app.models import (
    User,
    StudentProfile,
    CompanyProfile
)


@auth_bp.route("/register/student", methods=["POST"])
def register_student():

    data = request.get_json()

    email = data.get("email")

    if User.query.filter_by(email=email).first():
        return jsonify({
            "message":"Email already exists."
        }),400

    user = User(

        name=data["name"],

        email=email,

        password=generate_password_hash(
            data["password"]
        ),

        role="student"
    )

    db.session.add(user)

    db.session.flush()

    student = StudentProfile(

        user_id=user.id,

        student_id=data["student_id"],

        phone=data.get("phone"),

        branch=data.get("branch"),

        cgpa=data.get("cgpa"),

        graduation_year=data.get("graduation_year")
    )

    db.session.add(student)

    db.session.commit()

    return jsonify({
        "message":"Student registered successfully."
    }),201


@auth_bp.route("/register/company", methods=["POST"])
def register_company():

    data=request.get_json()

    email=data.get("email")

    if User.query.filter_by(email=email).first():

        return jsonify({
            "message":"Email already exists."
        }),400

    user=User(

        name=data["company_name"],

        email=email,

        password=generate_password_hash(
            data["password"]
        ),

        role="company"
    )

    db.session.add(user)

    db.session.flush()

    company=CompanyProfile(

        user_id=user.id,

        company_name=data["company_name"],

        hr_name=data.get("hr_name"),

        hr_email=data.get("hr_email"),

        phone=data.get("phone"),

        website=data.get("website"),

        description=data.get("description")
    )

    db.session.add(company)

    db.session.commit()

    return jsonify({
        "message":"Company registration submitted for approval."
    }),201


@auth_bp.route("/login", methods=["POST"])
def login():

    data=request.get_json()

    user=User.query.filter_by(
        email=data.get("email")
    ).first()

    if not user:

        return jsonify({
            "message":"Invalid email or password."
        }),401

    if not check_password_hash(
        user.password,
        data.get("password")
    ):

        return jsonify({
            "message":"Invalid email or password."
        }),401

    token=create_access_token(
        identity=str(user.id),
        additional_claims={
            "role":user.role
        }
    )

    return jsonify({

        "access_token":token,

        "role":user.role,

        "name":user.name

    })


@auth_bp.route("/me")
@jwt_required()
def me():

    user_id=get_jwt_identity()

    claims=get_jwt()

    return jsonify({

        "user_id":user_id,

        "role":claims["role"]

    })