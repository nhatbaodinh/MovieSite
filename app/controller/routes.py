from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/settings')
@main.route('/settings.html')
def settings():
    return render_template('settings.html')

# Các route khác theo danh sách bạn cung cấp
@main.route('/404')
@main.route('/404.html')
def not_found():
    return render_template('404.html'), 404

@main.route('/blank')
@main.route('/blank.html')
def blank():
    return render_template('blank.html')

@main.route('/history')
@main.route('/history-page.html')
def history_page():
    return render_template('history-page.html')

@main.route('/upload-video')
@main.route('/upload-video.html')
def upload_video():
    return render_template('upload-video.html')

@main.route('/video-page')
@main.route('/video-page.html')
def video_page():
    return render_template('video-page.html')