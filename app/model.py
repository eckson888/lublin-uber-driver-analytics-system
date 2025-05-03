from flask_login import UserMixin
from app.app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)    

    def __init__(self, username, password):
        self.username = username
        self.password = password