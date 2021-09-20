from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User
from app.api.errors import error_response

b_auth = HTTPBasicAuth()
t_auth = HTTPTokenAuth()

@b_auth.verify_password
def verify_password(username,password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)

@b_auth.error_handler
def basic_auth_error():
    return error_response(401)

@t_auth.verify_token
def verify_token(token):
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None

@t_auth.error_handler
def token_auth_error():
    return error_response(401)