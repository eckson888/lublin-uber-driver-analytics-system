from flask_login import UserMixin
from app.app import db
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    isVerified = db.Column(db.Boolean, nullable=False, default=False, server_default='false')
    uploads = relationship('RawData', back_populates='user')    

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.isVerified=False
        

class RawData(db.Model):
    __tablename__ = 'raw_data'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='uploads')

