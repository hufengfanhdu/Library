from ... import db
from ..user.model import User
import datetime


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, index=True)
    author = db.Column(db.String(25), nullable=False)
    publish = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    img = db.Column(
        db.String(100),
        nullable=False,
        default="books/default.jpg")
    category = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<{},{},{},{}>'.format(
            self.id,
            self.name,
            self.author,
            self.publish
        )

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'publish': self.publish,
            'price': self.price,
            'amount': self.amount,
            'img': self.img,
            'category': self.category
        }


class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, default=datetime.datetime.now)
    due = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String(8), db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    def get_user(self):
        return User.query.filter_by(id=self.user_id).first()

    def get_book(self):
        return Book.query.filter_by(id=self.book_id).first()

    def to_json(self):
        return {
            'id': self.id,
            'start': self.start,
            'due': self.due,
            'user': self.get_user,
            'book': self.get_book
        }
