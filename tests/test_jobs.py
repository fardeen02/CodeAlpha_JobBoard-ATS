import pytest
from app import create_app, db
from models.user import User
from flask_bcrypt import generate_password_hash


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


def create_recruiter(client):
    client.post(
        "/api/auth/register",
        json={
            "name": "Recruiter",
            "email": "recruiter@test.com",
            "password": "SecurePass123",
            "role": "recruiter"
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "recruiter@test.com",
            "password": "SecurePass123"
        }
    )

    return response.get_json()["access_token"]


def test_recruiter_can_create_job(client):
    token = create_recruiter(client)

    response = client.post(
        "/api/jobs",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Python Developer",
            "company": "TechNova",
            "location": "Kolkata",
            "description": "Build Flask APIs"
        }
    )

    assert response.status_code == 201


def test_create_job_without_token(client):
    response = client.post(
        "/api/jobs",
        json={
            "title": "Python Developer",
            "company": "TechNova",
            "location": "Kolkata",
            "description": "Build Flask APIs"
        }
    )

    assert response.status_code == 401


def test_create_job_missing_title(client):
    token = create_recruiter(client)

    response = client.post(
        "/api/jobs",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "company": "TechNova",
            "location": "Kolkata",
            "description": "Build Flask APIs"
        }
    )

    assert response.status_code == 400

def test_get_jobs_empty(client):
    response = client.get("/api/jobs")

    assert response.status_code == 200
    assert response.get_json()["jobs"] == []

def test_get_jobs_returns_jobs(client):
    token = create_recruiter(client)

    client.post(
        "/api/jobs",
        headers = {
            "Authorization": f"Bearer {token}"
            },
        json = {
            "title": "Python Developer",
            "company": "TechNova",
            "location": "Kolkata",
            "description": "Build Flask APIs",
            "salary": 600000,
            "employment_type": "Full-time"
            }
        )
    response = client.get("/api/jobs")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["jobs"]) == 1
    assert data["jobs"][0]["title"] == "Python Developer"
    assert data["jobs"][0]["company"] == "TechNova"
    assert data["jobs"][0]["location"] == "Kolkata"
    assert data["jobs"][0]["salary"] == 600000
    assert data["jobs"][0]["employment_type"] == "Full-time"

def test_get_single_job(client):
    token = create_recruiter(client)

    create_response = client.post(
        "/api/jobs",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Backend Developer",
            "company": "TechNova",
            "location": "Kolkata",
            "description": "Build APIs"
        }
    )

    job_id = create_response.get_json()["job"]["job_id"]

    response = client.get(f"/api/jobs/{job_id}")

    assert response.status_code == 200

    data = response.get_json()

    assert data["job"]["title"] == "Backend Developer"
    assert data["job"]["company"] == "TechNova"

def test_get_nonexistent_job(client):
    response = client.get("/api/jobs/999")

    assert response.status_code == 404

def test_owner_can_update_job(client):
    token = create_recruiter(client)

    create_response = client.post(
        "/api/jobs",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Backend Developer",
            "company": "TechNova",
            "location": "Kolkata",
            "description": "Build APIs"
        }
    )

    job_id = create_response.get_json()["job"]["job_id"]

    response = client.put(
        f"/api/jobs/{job_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"salary": 800000}
    )

    assert response.status_code == 200
    assert response.get_json()["job"]["salary"] == 800000

def test_update_job_without_token(client):
    response = client.put(
        "/api/jobs/1",
        json={"salary": 800000}
    )

    assert response.status_code == 401

def test_update_nonexistent_job(client):
    token = create_recruiter(client)

    response = client.put(
        "/api/jobs/999",
        headers={"Authorization": f"Bearer {token}"},
        json={"salary": 800000}
    )

    assert response.status_code == 404

def test_owner_can_delete_job(client):
    token = create_recruiter(client)

    create_response = client.post(
        "/api/jobs",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Backend Developer",
            "company": "TechNova",
            "location": "Kolkata",
            "description": "Build APIs"
        }
    )

    job_id = create_response.get_json()["job"]["job_id"]

    response = client.delete(
        f"/api/jobs/{job_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    check = client.get(f"/api/jobs/{job_id}")

    assert check.status_code == 404


def test_delete_job_without_token(client):
    response = client.delete("/api/jobs/1")

    assert response.status_code == 401


def test_delete_nonexistent_job(client):
    token = create_recruiter(client)

    response = client.delete(
        "/api/jobs/999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404



























    
























































