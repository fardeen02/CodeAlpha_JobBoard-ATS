from datetime import datetime, UTC
from app import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="jobseeker")
    skills = db.Column(db.Text)
    experience = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    jobs = db.relationship("Job", backref="recruiter", lazy=True)
    applications = db.relationship("Application", backref="applicant", lazy=True)
