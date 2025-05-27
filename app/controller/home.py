from flask import Blueprint, render_template
from flask import get_flashed_messages
from app.models.movie import Movie
from app.models.category import Category

home = Blueprint('home', __name__)

@home.route('/')
@home.route('/index.html')
def index():
    get_flashed_messages()
    movies = Movie.query.all()
    categories = Category.query.limit(10).all()
    return render_template('index.html', movies=movies, categories=categories)