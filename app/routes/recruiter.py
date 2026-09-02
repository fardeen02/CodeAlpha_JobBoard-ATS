from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from models.user import User

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
                "status": application.status
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
