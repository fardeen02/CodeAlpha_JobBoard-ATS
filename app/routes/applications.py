from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from app import db
from models.user import User
from models.job import Job
from models.application import Application
from app.utils.ats import (
    extract_text,
    extract_skills,
    calculate_match
)

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


@applications_bp.route("/applications/<int:app_id>/resume", methods=["POST"])
@jwt_required()
def upload_resume(app_id):
    user_id = int(get_jwt_identity())

    application = db.session.get(Application, app_id)

    if application is None:
        return jsonify({"error": "Application not found"}), 404

    if application.user_id != user_id:
        return jsonify({
            "error": "You can upload only your own resume"
        }), 403

    if "resume" not in request.files:
        return jsonify({
            "error": "Resume file is required"
        }), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected"
        }), 400

    filename = secure_filename(f"{app_id}_{file.filename}")

    upload_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )

    os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)

    file.save(upload_path)

    text = extract_text(upload_path)

    skills = extract_skills(text)

    score = calculate_match(
        application.job.skills_required or "",
        skills
    )

    application.resume_filename = filename
    application.resume_skills = ", ".join(skills)
    application.match_score = score

    db.session.commit()

    return jsonify({
    "message": "Resume uploaded successfully",
    "resume_filename": filename,
    "resume_skills": skills,
    "match_score": score,
    }), 200
































    

































