from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.category import Category
from app.models.movie import Movie
from app.models.db import db
from werkzeug.utils import secure_filename
from moviepy import VideoFileClip
from datetime import datetime
import os
import shutil

movie = Blueprint('movie', __name__)
UPLOAD_FOLDER = 'app/static/uploads/movies'

@movie.route('/movies')
@movie.route('/movies.html')
def movies_page():
    movies = Movie.query.all()
    categories = Category.query.all()
    return render_template('movie/movies.html', movies=movies, categories=categories)

@movie.route('/upload', methods=['GET'])
def upload_page():
    categories = Category.query.all()
    return render_template('movie/upload.html', categories=categories)

@movie.route('/upload', methods=['POST'])
def upload_movie():
    title = request.form['title']
    description = request.form['description']
    category_id = request.form['category']
    video_file = request.files.get('video_file')
    poster_file = request.files.get('poster_file')

    if not video_file or video_file.filename == '':
        flash("Vui lòng chọn video!", "danger")
        return redirect(url_for('movie.upload_page'))

    # Tạo thư mục lưu trữ
    safe_title = secure_filename(title)
    movie_folder = os.path.join(UPLOAD_FOLDER, safe_title)
    poster_folder = os.path.join(movie_folder, 'poster')
    os.makedirs(poster_folder, exist_ok=True)

    # Lưu video
    video_filename = secure_filename(video_file.filename)
    video_path = os.path.join(movie_folder, video_filename)
    video_file.save(video_path)
    video_url = f"/static/uploads/movies/{safe_title}/{video_filename}"

    # Lấy thời lượng video (tính theo phút)
    try:
        clip = VideoFileClip(video_path)
        duration_seconds = clip.duration
        duration_minutes = int(round(duration_seconds / 60))
        clip.reader.close()
        if clip.audio:
            clip.audio.reader.close_proc()
    except Exception as e:
        flash("Không thể lấy thời lượng video: " + str(e), "danger")
        return redirect(url_for('movie.upload_page'))

    # Lưu poster (nếu có)
    poster_url = None
    if poster_file and poster_file.filename != '':
        poster_filename = secure_filename(poster_file.filename)
        poster_path = os.path.join(poster_folder, poster_filename)
        poster_file.save(poster_path)
        poster_url = f"/static/uploads/movies/{safe_title}/poster/{poster_filename}"

    # Lưu thông tin phim vào CSDL
    movie = Movie(
        title=title,
        description=description,
        category_id=category_id,
        video_url=video_url,
        poster_url=poster_url,
        duration=duration_minutes,
        created_at=datetime.utcnow()
    )
    db.session.add(movie)
    db.session.commit()

    flash("Upload phim thành công!", "success")
    return redirect(url_for('movie.movies_page'))

@movie.route('/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(movie_id):
    movie_to_delete = Movie.query.get_or_404(movie_id)

    # Xóa toàn bộ thư mục chứa phim (bao gồm cả video và poster)
    try:
        movie_folder = os.path.join(UPLOAD_FOLDER, secure_filename(movie_to_delete.title))
        if os.path.exists(movie_folder):
            shutil.rmtree(movie_folder)
    except Exception as e:
        flash(f"Lỗi khi xóa thư mục phim: {e}", "danger")

    # Xóa khỏi database
    db.session.delete(movie_to_delete)
    db.session.commit()

    flash("Xóa phim thành công!", "success")
    return redirect(url_for('movie.movies_page'))

@movie.route('/movies/<int:movie_id>/edit', methods=['POST'])
def edit_movie(movie_id):
    movie_to_edit = Movie.query.get_or_404(movie_id)

    movie_to_edit.title = request.form['title']
    movie_to_edit.description = request.form['description']
    movie_to_edit.category_id = request.form['category_id']

    try:
        db.session.commit()
        flash('Cập nhật phim thành công!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Lỗi khi cập nhật phim: {e}', 'danger')

    return redirect(url_for('movie.movies_page'))