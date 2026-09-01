from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.user import User
from models.job import Job

jobs_bp = Blueprint("jobs",__name__, url_prefix="/api/jobs")

@jobs_bp.route("", methods=["POST"])
@jwt_required()
def create_job():
    user_id = int(get_jwt_identity())

    recruiter = db.session.get(User, user_id)

    if recruiter.role != "recruiter":
        return jsonify({
            "error": "Only recruiters can create jobs"
            }), 403

    data = request.get_json()

    required_fields = [
        "title",
        "company",
        "location",
        "description"
        ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "error": f"{field} is required"
                }), 400

    job = Job(
        title=data["title"],
        company=data["company"],
        location=data["location"],
        description=data["description"],
        skills_required=data.get("skills_required"),
        salary=data.get("salary"),
        employment_type=data.get("employment_type","Full-time"),
        recruiter_id=user_id
        )

    db.session.add(job)
    db.session.commit()

    return jsonify({
        "message": "Job created successfully",
        "job":{
            "job_id":job.job_id,
            "title": job.title,
            "company": job.company
            }
        }), 201

@jobs_bp.route("",methods=["GET"])
def get_jobs():
    jobs = Job.query.order_by(Job.created_at.desc()).all()

    return jsonify({
        "jobs": [
            {
                "job_id": job.job_id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "salary": job.salary,
                "employment_type": job.employment_type
            }
            for job in jobs
            ]
        }), 200

@jobs_bp.route("/<int:job_id>", methods=["GET"])
def get_job(job_id):
    job = db.session.get(Job, job_id)

    if job is None:
        return jsonify({"error": "Job not found"}), 404

    return jsonify({
        "job": {
            "job_id": job.job_id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "description": job.description,
            "skills_required": job.skills_required,
            "salary": job.salary,
            "employment_type": job.employment_type,
            "recruiter_id": job.recruiter_id
        }
    }), 200


@jobs_bp.route("/<int:job_id>", methods=["PUT"])
@jwt_required()
def update_job(job_id):
    user_id = int(get_jwt_identity())

    job = db.session.get(Job, job_id)

    if job is None:
        return jsonify({"error": "Job not found"}), 404

    if job.recruiter_id != user_id:
        return jsonify({
            "error": "You can only edit your own jobs"
        }), 403

    data = request.get_json()

    if "title" in data:
        job.title = data["title"]

    if "company" in data:
        job.company = data["company"]

    if "location" in data:
        job.location = data["location"]

    if "description" in data:
        job.description = data["description"]

    if "salary" in data:
        job.salary = data["salary"]

    if "employment_type" in data:
        job.employment_type = data["employment_type"]

    db.session.commit()

    return jsonify({
        "message": "Job updated successfully",
        "job": {
            "job_id": job.job_id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "salary": job.salary
        }
    }), 200


@jobs_bp.route("/<int:job_id>", methods=["DELETE"])
@jwt_required()
def delete_job(job_id):
    user_id = int(get_jwt_identity())

    job = db.session.get(Job, job_id)

    if job is None:
        return jsonify({"error": "Job not found"}), 404

    if job.recruiter_id != user_id:
        return jsonify({
            "error": "You can only delete your own jobs"
        }), 403

    db.session.delete(job)
    db.session.commit()

    return jsonify({
        "message": "Job deleted successfully"
    }), 200

























    
