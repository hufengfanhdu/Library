from flask import Blueprint, url_for, flash
from flask import render_template, redirect, request
from .verification import AddBookForm
from ..auth.auth import manager_required
from ..user.model import User
from ..book.model import Book, Borrow
from ... import db
from datetime import datetime, timedelta

bp = Blueprint('manager', __name__, url_prefix='/manager')


@bp.route('/')
@manager_required(3)
def show():
    users = User.query.all()
    return render_template('user/show_manager.html', users=users)


@bp.route('/delete/<string:id>', methods=['POST'])
@manager_required(3)
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    flash('用户注销成功', 'success')
    return redirect(url_for('manager.show'))


@bp.route('/book')
@manager_required(3)
def book():
    books = Book.query.all()
    return render_template('user/show_manager.html', books=books)


@bp.route('/deletebook/<string:id>', methods=['POST'])
@manager_required(3)
def delete_book(id):
    borrow = Borrow.query.filter_by(book_id=id).all()
    book = Book.query.filter_by(id=id).first()
    print(book)
    if len(borrow) > 0:
        flash('尚有图书借出，操作被禁止', 'danger')
    else:
        db.session.delete(book)
        db.session.commit()
        flash('图书下架成功', 'success')
    return redirect(url_for('manager.book'))


@bp.route('/book/add', methods=['GET', 'POST'])
@manager_required(3)
def add_book():
    form = AddBookForm(request.form)
    if request.method == "POST" and form.validate():
        name = request.form['name']
        author = request.form['author']
        publish = request.form['publish']
        price = request.form['price']
        amount = request.form['amount']
        category = request.form['category']
        book = Book(
            name=name,
            author=author,
            publish=publish,
            price=price,
            amount=amount,
            category=category
        )
        db.session.add(book)
        flash('图书录入成功', 'success')
        return redirect(url_for('manager.book'))
    return render_template('user/show_manager.html', form=form)


@bp.route('/borrow', methods=['POST'])
@manager_required(3)
def borrow():
    id = request.form['id']
    user = User.query.filter_by(id=id).first()
    if request.method == 'POST' and id:
        book_id = request.form['book_id']
        book = Book.query.filter_by(id=book_id).first()
        identity = user.get_detail()
        borrows = Borrow.query.filter_by(user_id=id).all()
        books = Borrow.query.filter_by(book_id=book_id).all()
        if len(borrows) < identity.borrow_num and len(books) < book.amount:
            start = datetime.now()
            due = datetime.now() + timedelta(days=identity.duration)
            borrow = Borrow(user_id=id, book_id=book_id, start=start, due=due)
            db.session.add(borrow)
            flash('书籍借阅成功', 'success')
        else:
            flash('借阅已达上限', 'warning')
    else:
        flash('操作失败', 'warning')
    return redirect(url_for('manager.show'))


@bp.route('/borrow')
@manager_required(3)
def show_borrow():
    id = request.args.get('id')
    borrows = Borrow.query.filter_by(user_id=id).all()
    now = datetime.now()
    return render_template('user/show_manager.html', borrows=borrows, now=now)


@bp.route('/renew', methods=['POST'])
@manager_required(3)
def renew():
    id = request.form['id']
    borrow = Borrow.query.filter_by(id=id).first()
    user = borrow.get_user()
    identity = user.get_detail()
    borrow.start = datetime.now()
    borrow.due = datetime.now() + timedelta(days=identity.duration)
    flash('续借成功', 'success')
    return redirect(url_for('manager.show'))


@bp.route('/delete/<int:id>', methods=['POST'])
@manager_required(3)
def delete_borrow(id):
    borrow = Borrow.query.filter_by(id=id).first()
    db.session.delete(borrow)
    flash('图书归还成功', 'success')
    return redirect(url_for('manager.show'))
