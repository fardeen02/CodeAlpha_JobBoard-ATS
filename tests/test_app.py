from app import create_app


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test-secret-key"
    JWT_SECRET_KEY = "test-jwt-secret-key"


def test_home_route():
    app = create_app(TestConfig)
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
