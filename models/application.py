from datetime import datetime, UTC
from app import db


class Application(db.Model):
    __tablename__ = "applications"

    app_id = db.Column(db.Integer, primary_key=True)

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.job_id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    applied_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(UTC)
    )
