from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from models.user import User
from models.application import Application

recruiter_bp = Blueprint(
    "recruiter",
    __name__,
    url_prefix="/api/recruiter"
)


@recruiter_bp.route("/applicants", methods=["GET"])
@jwt_required()
def get_applicants():
    user_id = int(get_jwt_identity())

    recruiter = db.session.get(User, user_id)

    if recruiter.role != "recruiter":
        return jsonify({
            "error": "Only recruiters can access this"
        }), 403

    jobs_data = []

    for job in recruiter.jobs:
        applicants = []

        for application in job.applications:
            applicants.append({
                "app_id": application.app_id,
                "name": application.applicant.name,
                "email": application.applicant.email,
                "status": application.status,
                "resume_skills": application.resume_skills,
                "match_score": application.match_score
                })

        jobs_data.append({
            "job_id": job.job_id,
            "title": job.title,
            "company": job.company,
            "total_applicants": len(applicants),
            "applicants": applicants
        })

    return jsonify({
        "jobs": jobs_data
    }), 200

@recruiter_bp.route("/applications/<int:app_id>/status", methods=["PATCH"])
@jwt_required()
def update_application_status(app_id):
    user_id = int(get_jwt_identity())

    recruiter = db.session.get(User, user_id)

    if not recruiter:
        return jsonify({
            "error": "Recruiter not found"
            }), 404

    if recruiter.role!="recruiter":
        return jsonify({
            "error": "Only recruiters can update applications"
            }), 403

    application = db.session.get(Application, app_id)

    if not application:
        return jsonify({
            "error": "Application not found"
            }), 404

    if application.job.recruiter_id != user_id:
        return jsonify({
            "error": "You can only update applications for your own jobs"
            }), 403

    data = request.get_json()

    if not data or "status" not in data:
        return jsonify({
            "error": "Status is required"
            }), 400

    status = data["status"].lower()

    allowed_statuses = ["accepted", "rejected"]

    if status not in allowed_statuses:
        return jsonify({
            "error": "Status must be accepted or rejected"
            }), 400

    application.status = status

    db.session.commit()

    return jsonify({
        "message": f"Application {status} successfully",
        "application": {
            "app_id": application.app_id,
            "status": application.status
            }
        }), 200

        

        

        





























        

























