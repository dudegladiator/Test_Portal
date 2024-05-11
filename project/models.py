from flask_login import UserMixin
from werkzeug.security import check_password_hash
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True)
    name = db.Column(db.String(80), unique=False)
    pwd_hash = db.Column(db.String(200))
    urole = db.Column(db.String(80))

    def __init__(self, email, name, pwd_hash, urole):
        self.email = email
        self.name = name
        self.pwd_hash = pwd_hash
        self.urole = urole

    def check_password(self, password):
        return check_password_hash(self.pwd_hash, password)

    def get_id(self):
        return self.id

    def get_urole(self):
        return self.urole
