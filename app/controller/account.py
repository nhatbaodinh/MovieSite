from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from app.models.user import User
from app.models.db import db

account = Blueprint('account', __name__)

@account.route('/account', methods=['GET', 'POST'])
@account.route('/account.html', methods=['GET', 'POST'])
def account_page():
    if 'username' not in session:
        flash('Vui lòng đăng nhập để tiếp tục.', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        user = User.query.filter_by(username=session.get('username')).first()

        if not user or not user.check_password(current_password):
            flash('Mật khẩu hiện tại không đúng.', 'danger')
            return redirect(url_for('account.account_page'))

        if new_password != confirm_password:
            flash('Mật khẩu mới và xác nhận mật khẩu không khớp.', 'danger')
            return redirect(url_for('account.account_page'))

        user.set_password(new_password)
        db.session.commit()
        flash('Đổi mật khẩu thành công.', 'success')
        return redirect(url_for('account.account_page'))

    return render_template('account/account.html')