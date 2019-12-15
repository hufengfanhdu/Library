from ... import db, login_manager
import datetime


class User(db.Model):
    '''
        Model for User.
    '''

    id = db.Column(db.String(8), primary_key=True)
    username = db.Column(db.String(25), nullable=False, index=True)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    identity = db.Column(db.Integer, db.ForeignKey('identity.id'))

    def __repr__(self):
        return '<{},{},{}>'.format(
            self.id,
            self.username,
            self.phone)

    def to_json(self):
        return {
            'username': self.username,
            'phone': self.phone,
            'id': self.id,
            'created_at': self.created_at,
            'identity': self.identity
        }

    def get_detail(self):
        identity = Identity.query.filter_by(id=self.identity).first()
        return identity

    def is_authenticated(self):
        return True

    def is_active(slef):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()


class Identity(db.Model):
    '''
        Model for Identity.
        ``Type: 0-Student, 1-Teacher, 2-Manager``
    '''

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    borrow_num = db.Column(db.Integer, nullable=False)
    fine = db.Column(db.Float, nullable=False)
    users = db.relationship('User', backref='user_identity', lazy="dynamic")

    def __repr__(self):
        return '<{},{},{},{}>'.format(
            self.type,
            self.duration,
            self.borrow_num,
            self.fine)

    def to_json(self):
        return {
            'type': self.type,
            'duration': self.duration,
            'borrow_num': self.borrow_num,
            'fine': self.fine
        }
