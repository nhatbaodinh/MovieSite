from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import User
from app.models.db import db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
@auth.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Tên tài khoản đã tồn tại.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, role='user')
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Đăng ký thành công. Bạn có thể đăng nhập.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth.route('/login', methods=['GET', 'POST'])
@auth.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = user.username
            session['role'] = user.role
            session['created_at'] = user.created_at.strftime('%d/%m/%Y')
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('home.index'))  # chuyển về trang chủ
        else:
            flash('Tên tài khoản hoặc mật khẩu sai.', 'danger')

    return render_template('auth/login.html')


@auth.route('/logout')
@auth.route('/logout.html')
def logout():
    session.clear()
    flash('Đã đăng xuất.', 'info')
    return redirect(url_for('auth.login'))