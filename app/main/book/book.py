from flask import Blueprint, render_template, request
from ..book.model import Book, Borrow
# from flask_login import login_user


bp = Blueprint('book', __name__, url_prefix='/book')


@bp.route('/', methods=['GET', 'POST'])
def show_book():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        category = request.args.get('category', None, type=str)
        if category:
            pagination = Book.query.filter_by(category=category).paginate(
                page, per_page=9,
                error_out=True)
        else:
            pagination = Book.query.paginate(
                page, per_page=9,
                error_out=True)
        books = pagination.items
    elif request.method == 'POST':
        search = request.form['search']
        pagination = Book.query.filter(Book.name.like('%'+search+'%')).paginate(
                1,
                per_page=9,
                error_out=True
            )
        books = pagination.items
    return render_template('book/show.html', books=books, pagination=pagination)


@bp.route('/<int:id>')
def book(id):
    book = Book.query.filter_by(id=id).first()
    borrows = Borrow.query.filter_by(book_id=id).all()
    return render_template('book/book.html', book=book, borrows=borrows)
