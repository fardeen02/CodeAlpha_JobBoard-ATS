from datetime import datetime, UTC
from app import db

class Job(db.Model):
    __tablename__ = "jobs"

    job_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills_required = db.Column(db.Text)
    salary = db.Column(db.Integer)
    employment_type = db.Column(db.String(30), default="Full-time")
    recruiter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

