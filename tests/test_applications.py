import pytest
from app import create_app, db


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test-secret-key-32-characters-long"
    JWT_SECRET_KEY = "abcdefghijklmnopqrstuvwxyz123456"


@pytest.fixture
def client():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.drop_all()


def create_user(client, role, email):
    client.post(
        "/api/auth/register",
        json={
            "name": role.title(),
            "email": email,
            "password": "SecurePass123",
            "role": role
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "SecurePass123"
        }
    )

    return response.get_json()["access_token"]


def create_job(client, recruiter_token):
    response = client.post(
        "/api/jobs",
        headers={"Authorization": f"Bearer {recruiter_token}"},
        json={
            "title": "Python Developer",
            "company": "TechNova",
            "location": "Kolkata",
            "description": "Build Flask APIs"
        }
    )

    return response.get_json()["job"]["job_id"]
def test_jobseeker_can_apply(client):
    recruiter = create_user(client, "recruiter", "rec@test.com")
    seeker = create_user(client, "jobseeker", "seek@test.com")

    job_id = create_job(client, recruiter)

    response = client.post(
        f"/api/jobs/{job_id}/apply",
        headers={"Authorization": f"Bearer {seeker}"}
    )

    assert response.status_code == 201
    assert response.get_json()["application"]["status"] == "Pending"

def test_recruiter_cannot_apply(client):
    recruiter = create_user(client, "recruiter", "rec@test.com")

    job_id = create_job(client, recruiter)

    response = client.post(
        f"/api/jobs/{job_id}/apply",
        headers={"Authorization": f"Bearer {recruiter}"}
    )

    assert response.status_code == 403

def test_duplicate_application(client):
    recruiter = create_user(client, "recruiter", "rec@test.com")
    seeker = create_user(client, "jobseeker", "seek@test.com")

    job_id = create_job(client, recruiter)

    client.post(
        f"/api/jobs/{job_id}/apply",
        headers={"Authorization": f"Bearer {seeker}"}
    )

    response = client.post(
        f"/api/jobs/{job_id}/apply",
        headers={"Authorization": f"Bearer {seeker}"}
    )

    assert response.status_code == 409

def test_apply_nonexistent_job(client):
    seeker = create_user(client, "jobseeker", "seek@test.com")

    response = client.post(
        "/api/jobs/999/apply",
        headers={"Authorization": f"Bearer {seeker}"}
    )

    assert response.status_code == 404

def test_apply_without_token(client):
    response = client.post("/api/jobs/1/apply")

    assert response.status_code == 401


        





































        
