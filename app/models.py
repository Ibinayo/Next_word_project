from flask_login import UserMixin
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """User class for database"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    username = db.Column(db.String(64), index=True, unique=True,
                         nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password_hash(self, password):
        """Generate password hash"""
        self.password_hash = generate_password_hash(password)


class Input(db.Model):
    """INput class for user inputs"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    input = db.Column(db.String(530), index=True, nullable=False)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
