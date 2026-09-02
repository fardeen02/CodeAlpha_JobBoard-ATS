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
        headers={
            "Authorization": f"Bearer {recruiter_token}"
        },
        json={
            "title": "Python Developer",
            "company": "TechNova",
            "location": "Kolkata",
            "description": "Build Flask APIs"
        }
    )

    return response.get_json()["job"]["job_id"]

def test_recruiter_can_view_applicants(client):
    recruiter = create_user(client, "recruiter", "rec@test.com")
    seeker = create_user(client, "jobseeker", "seek@test.com")

    job_id = create_job(client, recruiter)

    client.post(
        f"/api/jobs/{job_id}/apply",
        headers={
            "Authorization": f"Bearer {seeker}"
        }
    )

    response = client.get(
        "/api/recruiter/applicants",
        headers={
            "Authorization": f"Bearer {recruiter}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["jobs"]) == 1
    assert data["jobs"][0]["job_id"] == job_id
    assert data["jobs"][0]["total_applicants"] == 1
    assert data["jobs"][0]["applicants"][0]["email"] == "seek@test.com"

def test_jobseeker_cannot_view_dashboard(client):
    seeker = create_user(client, "jobseeker", "seek@test.com")

    response = client.get(
        "/api/recruiter/applicants",
        headers={
            "Authorization": f"Bearer {seeker}"
        }
    )

    assert response.status_code == 403

def test_recruiter_with_no_jobs(client):
    recruiter = create_user(client, "recruiter", "rec@test.com")

    response = client.get(
        "/api/recruiter/applicants",
        headers={
            "Authorization": f"Bearer {recruiter}"
        }
    )

    assert response.status_code == 200
    assert response.get_json()["jobs"] == []





























































        
