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





























    
