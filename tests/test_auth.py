import pytest
from app import create_app, db


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test-jwt-secret-key-32-characters-long"
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


def test_register_user(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "SecurePass123",
            "role": "jobseeker",
            "skills": "Python, Flask",
            "experience": 1
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["message"] == "User registered successfully"
    assert data["user"]["email"] == "test@example.com"


def test_register_missing_password(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com"
        }
    )

    assert response.status_code == 400


def test_register_duplicate_email(client):
    user = {
        "name": "Test User",
        "email": "duplicate@example.com",
        "password": "SecurePass123"
    }

    first_response = client.post(
        "/api/auth/register",
        json=user
    )

    second_response = client.post(
        "/api/auth/register",
        json=user
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409

def test_password_is_hashed(client):
    client.post(
        "/api/auth/register",
        json={
            "name": "Security Test",
            "email": "security@example.com",
            "password": "MySecret123"
        }
    )

    from models.user import User

    user = User.query.filter_by(
        email="security@example.com"
    ).first()

    assert user is not None
    assert user.password != "MySecret123"
    assert user.password.startswith("$2")

def test_register_missing_name(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "noname@example.com",
            "password": "SecurePass123"
        }
    )

    assert response.status_code == 400

def test_register_missing_email(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "No Email",
            "password": "SecurePass123"
        }
    )

    assert response.status_code == 400

def test_login_success(client):
    client.post(
        "/api/auth/register",
        json = {
            "name": "Login User",
            "email": "login@example.com",
            "password": "SecurePass123"
            }
        )

    response = client.post(
        "/api/auth/login",
        json = {
            "email": "login@example.com",
            "password": "SecurePass123"
            }
        )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Login successful"
    assert "access_token" in data
    assert data["user"]["email"] == "login@example.com"

def test_profile_with_valid_token(client):
    client.post("/api/auth/register",
                json = {
                    "name": "Profile User",
                    "email": "profile@example.com",
                    "password": "SecurePass123"
                    }
                )

    login_response = client.post(
        "/api/auth/login",
        json = {
            "email": "profile@example.com",
            "password": "SecurePass123"
            }
        )

    login_data = login_response.get_json()
    token = login_data["access_token"]

    response = client.get(
        "api/auth/profile",
        headers = {
            "Authorization": f"Bearer {token}"
            }
        )

    assert response.status_code == 200

    data = response.get_json()

    assert data["user"]["email"] == "profile@example.com"
    assert data["user"]["name"] == "Profile User"

def test_profile_without_token(client):
    response = client.get("/api/auth/profile")

    assert response.status_code == 401






