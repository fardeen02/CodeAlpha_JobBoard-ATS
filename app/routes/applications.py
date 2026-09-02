from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.user import User
from models.job import Job
from models.application import Application

applications_bp = Blueprint("applications", __name__, url_prefix="/api/jobs")

@applications_bp.route("/<int:job_id>/apply", methods=["POST"])
@jwt_required()
def apply_job(job_id):
    user_id = int(get_jwt_identity())

    user = db.session.get(User, user_id)

    if user.role != "jobseeker":
        return jsonify({
            "error": "Only job seekers can apply"
            }), 403

    job = db.session.get(Job, job_id)

    if job is None:
        return jsonify({
            "error": "Job not found"
            }), 404

    existing = Application.query.filter_by(
        job_id = job_id,
        user_id=user_id
        ).first()

    if existing:
        return jsonify({
            "error": "You have already applied"
            }), 409

    application = Application(
        job_id=job_id,
        user_id=user_id
        )

    db.session.add(application)
    db.session.commit()

    return jsonify({
        "message": "Application submitted successfully",
        "application": {
            "app_id": application.app_id,
            "job_id": application.job_id,
            "status": application.status
            }
        }), 201

    
































    

































