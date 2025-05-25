from flask import Flask
from .models import db
from .routes import main
import os

def create_app():
    app = Flask(__name__)

    # Load cấu hình từ file config.py
    app.config.from_pyfile('config.py')

    # Khởi tạo SQLAlchemy
    db.init_app(app)

    # Đăng ký blueprint
    app.register_blueprint(main)

    return app