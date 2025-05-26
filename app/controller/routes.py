from flask import Blueprint, render_template
from app.models.movie import Movie
from app.models.category import Category

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index.html')
def index():
    movies = Movie.query.all()
    categories = Category.query.all()
    return render_template('index.html', movies=movies, categories=categories)

@main.route('/settings')
@main.route('/settings.html')
def settings():
    return render_template('settings.html')

# Các route khác theo danh sách bạn cung cấp
@main.route('/404')
@main.route('/404.html')
def not_found():
    return render_template('404.html'), 404

@main.route('/account')
@main.route('/account.html')
def account():
    return render_template('account.html')

@main.route('/categories')
@main.route('/categories.html')
def categories():
    return render_template('categories.html')

@main.route('/blank')
@main.route('/blank.html')
def blank():
    return render_template('blank.html')

@main.route('/channels')
@main.route('/channels.html')
def channels():
    return render_template('channels.html')

@main.route('/forgot-password')
@main.route('/forgot-password.html')
def forgot_password():
    return render_template('forgot-password.html')

@main.route('/history')
@main.route('/history-page.html')
def history_page():
    return render_template('history-page.html')

@main.route('/shop')
@main.route('/shop.html')
def shop():
    return render_template('shop.html')

@main.route('/single-channel')
@main.route('/single-channel.html')
def single_channel():
    return render_template('single-channel.html')

@main.route('/subscriptions')
@main.route('/subscriptions.html')
def subscriptions():
    return render_template('subscriptions.html')

@main.route('/upload')
@main.route('/upload.html')
def upload():
    return render_template('upload.html')

@main.route('/upload-video')
@main.route('/upload-video.html')
def upload_video():
    return render_template('upload-video.html')

@main.route('/video')
@main.route('/video-page.html')
def video_page():
    return render_template('video-page.html')