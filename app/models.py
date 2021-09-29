from app import db, login_manager
from flask_login import UserMixin
from flask import current_app as app
from time import time
from datetime import datetime, timedelta
import os
import base64
import jwt
from app import bcrypt

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    passwords = db.relationship("Password", backref="author", lazy=True)
    token = db.Column(db.String(32),index=True,unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return f"{self.id} {self.username} {self.email} {self.password}"

    def change_email(self, new_email):
        self.email = new_email

    def set_password(self, password):
        self.password = password

    def get_reset_password_token(self, expires=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time()+expires},
            app.config["SECRET_KEY"], algorithm="HS256"
        )

    @staticmethod
    def verify_token(token):
        try:
            id = jwt.decode(
                token, app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )['reset_password']
        except:
            return
        return User.query.get(id)

    def to_dict(self):
        data = {
            "id":self.id,
            "username":self.username,
            "email":self.email
        }
        return data
    
    def from_dict(self,data):
        for field in ["username","email"]:
            if field in data:
                setattr(self,field,data[field])
        if "password" in data:
            self.set_password(bcrypt.generate_password_hash(
            data["password"]).decode('utf-8'))
            

    def get_token(self,expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now+timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode("utf-8")
        self.token_expiration = now+timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow()-timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def check_password(self,password):
        return bcrypt.check_password_hash(self.password,password)

class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_name = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    password_content = db.Column(db.String(120), nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"{self.id} {self.password_name} {self.date_added} {self.password_content}"

    def change_password(self, new_password):
        self.password_content = new_password
    
    def to_dict(self):
        data = {
            "password_name":self.password_name,
            "content":self.password_content,
            "created":self.date_added
        }
        return data
