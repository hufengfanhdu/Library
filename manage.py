import os
from app import create_app, db
from flask_script import Manager, Shell
from app.main.user.model import User, Identity
from app.main.book.model import Book

app = create_app(os.getenv('FLASK_CONFIG') or 'development')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Identity=Identity, Book=Book)


manager.add_command('shell', Shell(make_context=make_shell_context))


if __name__ == "__main__":
    manager.run()
