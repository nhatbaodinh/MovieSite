from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, get_flashed_messages
from app.models.category import Category
from app.models.db import db

category = Blueprint('category', __name__)

@category.route('/categories')
@category.route('/categories.html')
def categories_page():
    categories = Category.query.all()
    return render_template('category/categories.html', categories=categories)

@category.route('/categories/add', methods=['POST'])
def add_category():
    name = request.form.get('name', '').strip()

    if not name:
        return jsonify({'error': 'Tên không được để trống'}), 400

    # Kiểm tra trùng tên với các thể loại khác
    existing = Category.query.filter_by(name=name).first()
    if existing:
        return jsonify({'error': 'Tên thể loại đã tồn tại'}), 400

    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()
    flash('Thêm thể loại thành công.', 'success')
    return jsonify({'message': 'Thêm thể loại thành công'})

@category.route('/categories/<int:category_id>/edit', methods=['POST'])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    name = request.form.get('name', '').strip()

    if not name:
        return jsonify({'error': 'Tên không được để trống'}), 400

    # Kiểm tra trùng tên với các thể loại khác (ngoại trừ chính nó)
    existing = Category.query.filter(Category.name == name, Category.id != category_id).first()
    if existing:
        return jsonify({'error': 'Tên thể loại đã tồn tại'}), 400

    category.name = name
    db.session.commit()
    flash('Cập nhật thành công.', 'success')
    return jsonify({'message': 'Cập nhật thành công'})

@category.route('/categories/<int:category_id>/delete', methods=['POST', 'GET'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)

    # Nếu thể loại đang có phim thì không cho xóa
    if category.movies:
        flash('Không thể xóa thể loại vì có phim thuộc thể loại này.', 'danger')
        return redirect(url_for('category.categories_page'))

    db.session.delete(category)
    db.session.commit()
    flash('Xóa thể loại thành công.', 'success')
    return redirect(url_for('category.categories_page'))