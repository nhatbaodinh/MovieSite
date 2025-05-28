from flask import Flask
from flask_migrate import Migrate
from app.models.db import db
from app.controller.auth import auth
from app.controller.routes import main
from app.controller.home import home
from app.controller.account import account
from app.controller.category import category
from app.controller.movie import movie_bp

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'kasperdinh'

    # Load configuration from config.py
    app.config.from_pyfile('config.py')

    # Initialize SQLAlchemy and Flask-Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # List of blueprints to register
    blueprints = [home, auth, account, category, movie_bp, main]

    # Register all blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app