from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename

from app.controller.category import category
from app.models.category import Category
from app.models.movie import Movie
from app.models.db import db
from moviepy import VideoFileClip
from datetime import datetime

import os
import shutil

movie_bp = Blueprint('movie_bp', __name__)
UPLOAD_FOLDER = 'app/static/uploads/movies'

@movie_bp.route('/movies')
@movie_bp.route('/movies.html')
def movies_page():
    if session['role'] != 'admin':
        return redirect(url_for('home.index'))

    movies = Movie.query.all()
    categories = Category.query.all()
    return render_template('movie/movies.html', movies=movies, categories=categories)

@movie_bp.route('/upload', methods=['GET'])
def upload_page():
    # Check if the user is an admin
    if session['role'] != 'admin':
        return redirect(url_for('home.index'))

    categories = Category.query.all()
    return render_template('movie/upload.html', categories=categories)

@movie_bp.route('/upload', methods=['POST'])
def upload_movie():
    # Check if the user is an admin
    if session['role'] != 'admin':
        return redirect(url_for('home.index'))

    title = request.form['title']
    description = request.form['description']
    category_id = request.form['category']
    video_file = request.files.get('video_file')
    poster_file = request.files.get('poster_file')

    if not title or not description or not category_id:
        return redirect(url_for('movie_bp.upload_page'))

    if not video_file or video_file.filename == '':
        flash("Vui lòng chọn video!", "danger")
        return redirect(url_for('movie_bp.upload_page'))

    safe_title = secure_filename(title)
    movie_folder = os.path.join(UPLOAD_FOLDER, safe_title)
    poster_folder = os.path.join(movie_folder, 'poster')
    os.makedirs(poster_folder, exist_ok=True)

    # Lưu video
    video_filename = secure_filename(video_file.filename)
    video_path = os.path.join(movie_folder, video_filename)
    video_file.save(video_path)
    video_url = f"/static/uploads/movies/{safe_title}/{video_filename}"

    # Lấy thời lượng video
    try:
        clip = VideoFileClip(video_path)
        duration_seconds = clip.duration
        duration_minutes = int(round(duration_seconds / 60))
    except Exception as e:
        flash("Không thể lấy thời lượng video: " + str(e), "danger")
        return redirect(url_for('movie_bp.upload_page'))
    finally:
        clip.close()

    # Lưu poster
    poster_url = None
    if poster_file and poster_file.filename != '':
        poster_filename = secure_filename(poster_file.filename)
        poster_path = os.path.join(poster_folder, poster_filename)
        poster_file.save(poster_path)
        poster_url = f"/static/uploads/movies/{safe_title}/poster/{poster_filename}"

    # Lưu thông tin phim
    new_movie = Movie(
        title=title,
        description=description,
        category_id=category_id,
        video_url=video_url,
        poster_url=poster_url,
        duration=duration_minutes,
        created_at=datetime.utcnow()
    )
    db.session.add(new_movie)
    db.session.commit()

    flash("Upload phim thành công!", "success")
    return redirect(url_for('movie_bp.movies_page'))

@movie_bp.route('/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(movie_id):
    # Check if the user is an admin
    if session['role'] != 'admin':
        return redirect(url_for('home.index'))

    movie_to_delete = Movie.query.get_or_404(movie_id)
    try:
        movie_folder = os.path.join(UPLOAD_FOLDER, secure_filename(movie_to_delete.title))
        if os.path.exists(movie_folder):
            shutil.rmtree(movie_folder)
    except Exception as e:
        flash(f"Lỗi khi xóa thư mục phim: {e}", "danger")

    db.session.delete(movie_to_delete)
    db.session.commit()
    flash("Xóa phim thành công!", "success")
    return redirect(url_for('movie_bp.movies_page'))

@movie_bp.route('/movies/<int:movie_id>/edit', methods=['POST'])
def edit_movie(movie_id):
    # Check if the user is an admin
    if session['role'] != 'admin':
        return redirect(url_for('home.index'))

    movie_to_edit = Movie.query.get_or_404(movie_id)
    old_title = movie_to_edit.title
    new_title = request.form['title']
    description = request.form['description']
    category_id = request.form['category_id']
    poster_file = request.files.get('poster')

    if not new_title or not description or not category_id:
        flash("Vui lòng điền đầy đủ thông tin!", "danger")
        return redirect(url_for('movie_bp.movies_page'))

    try:
        if old_title != new_title:
            old_folder = os.path.join(UPLOAD_FOLDER, secure_filename(old_title))
            new_folder = os.path.join(UPLOAD_FOLDER, secure_filename(new_title))
            if os.path.exists(new_folder):
                flash("Tên phim mới đã tồn tại, vui lòng chọn tên khác!", "danger")
                return redirect(url_for('movie_bp.movies_page'))
            if os.path.exists(old_folder):
                os.rename(old_folder, new_folder)

            # Cập nhật URL video và poster
            if movie_to_edit.video_url:
                video_name = os.path.basename(movie_to_edit.video_url)
                movie_to_edit.video_url = f"/static/uploads/movies/{secure_filename(new_title)}/{video_name}"
            if movie_to_edit.poster_url:
                poster_name = os.path.basename(movie_to_edit.poster_url)
                movie_to_edit.poster_url = f"/static/uploads/movies/{secure_filename(new_title)}/poster/{poster_name}"

        # Lưu poster mới nếu có
        if poster_file and poster_file.filename != '':
            poster_folder = os.path.join(UPLOAD_FOLDER, secure_filename(new_title), 'poster')
            os.makedirs(poster_folder, exist_ok=True)

            poster_filename = secure_filename(poster_file.filename)
            poster_path = os.path.join(poster_folder, poster_filename)

            # Xoá poster cũ trước khi cập nhật URL
            if movie_to_edit.poster_url:
                old_poster_path = os.path.join(UPLOAD_FOLDER, secure_filename(old_title), 'poster', os.path.basename(movie_to_edit.poster_url))
                if os.path.exists(old_poster_path):
                    os.remove(old_poster_path)

            poster_file.save(poster_path)
            movie_to_edit.poster_url = f"/static/uploads/movies/{secure_filename(new_title)}/poster/{poster_filename}"

        # Cập nhật các trường còn lại
        movie_to_edit.title = new_title
        movie_to_edit.description = description
        movie_to_edit.category_id = category_id

        db.session.commit()
        flash('Cập nhật phim thành công!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Lỗi khi cập nhật phim: {e}', 'danger')

    return redirect(url_for('movie_bp.movies_page'))

@movie_bp.route('/movies/<int:movie_id>/details')
@movie_bp.route('/movies/<int:movie_id>/details.html')
def movie_details(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template('movie/movie_details.html', movie=movie)

@movie_bp.route('/single-movie/<int:movie_id>', methods=['GET'])
def single_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # Fetch the movie by ID
    return render_template('movie/single_movie.html', movie=movie)

@movie_bp.route('/movies/search', methods=['GET'])
def search_movies():
    keyword = request.args.get('q', '').strip()
    categories = Category.query.limit(10).all()

    if not keyword:
        flash('Vui lòng nhập từ khóa tìm kiếm!', 'warning')
        return redirect(url_for('movie_bp.movies_page'))

    movies = Movie.query.filter(
        Movie.title.ilike(f'%{keyword}%') | Movie.description.ilike(f'%{keyword}%')
    ).all()

    return render_template('index.html', movies=movies, keyword=keyword, categories=categories)

@movie_bp.route('/movies/category/<string:category_name>')
def movies_by_category(category_name):
    # Tìm thể loại theo tên
    category = Category.query.filter_by(name=category_name).first_or_404()

    # Tìm phim theo category_id
    movies = Movie.query.filter_by(category_id=category.id).all()

    # Lấy danh sách tất cả thể loại
    categories = Category.query.limit(10).all()

    return render_template(
        'index.html',
        movies=movies,
        categories=categories,
        selected_category=category.id
    )