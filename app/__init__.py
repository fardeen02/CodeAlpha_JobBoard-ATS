from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_class=None):
    app = Flask(__name__)

    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_object("config.Config")

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from models.user import User
    from models.job import Job
    from models.application import Application
    from app.routes.auth import auth_bp
    from app.routes.jobs import jobs_bp
    from app.routes.applications import applications_bp
    
    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        return jsonify({
            "project": "Job Board & Mini ATS API",
            "status": "Running",
            "version": "1.0"
        })

    app.register_blueprint(jobs_bp)
    app.register_blueprint(applications_bp)
    
    return app
