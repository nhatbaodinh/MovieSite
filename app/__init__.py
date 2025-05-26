from flask import Flask
from flask_migrate import Migrate
from app.models.db import db
from app.controller.auth import auth
from app.controller.routes import main

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'kasperdinh'

    # Load cấu hình từ file config.py
    app.config.from_pyfile('config.py')

    # Khởi tạo SQLAlchemy và Flask-Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Đăng ký blueprint
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app