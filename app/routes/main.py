from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("index.html")

@main_bp.route("/login")
def login_page():
    return render_template("login.html")

@main_bp.route("/register")
def register_page():
    return render_template("register.html")

@main_bp.route("/jobs")
def jobs_page():
    return render_template("jobs.html")

@main_bp.route("/jobs/<int:job_id>")
def job_details_page(job_id):
    return render_template("job_details.html", job_id=job_id)

@main_bp.route("/recruiter")
def recruiter_dashboard():
    return render_template("recruiter_dashboard.html")

@main_bp.route("/recruiter/create-job")
def create_job_page():
    return render_template("create_job.html")

@main_bp.route("/about")
def about_page():
    return render_template("about.html")

@main_bp.route("/features")
def features_page():
    return render_template("features.html")

from flask import jsonify
from models.user import User
from models.job import Job
from models.application import Application
from app import db

@main_bp.route("/api/stats")
def get_stats():
    total_jobs = Job.query.count()
    total_recruiters = User.query.filter_by(role="recruiter").count()
    total_applicants = Application.query.count()
    avg_score = db.session.query(
        db.func.avg(Application.match_score)
        ).scalar() or 0

    return jsonify({
        "jobs": total_jobs,
        "recruiters": total_recruiters,
        "applicants": total_applicants,
        "accuracy": round(avg_score)
    })
