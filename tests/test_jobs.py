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
