from werkzeug.wrappers import response
from app.api import api
from app.models import User, Password
from flask import jsonify, request
from app.api.auth import t_auth
<<<<<<< HEAD
from flask import g
=======
from app.api.errors import bad_request
from flask import g
from app import db
>>>>>>> b08e2d9fc7004f5c781600c8cef8dc8d0afe57a0


@api.route("/users/<int:id>", methods=['GET'])
@t_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@api.route("/users", methods=['GET'])
@t_auth.login_required
def get_users():
    users = User.query.all()
    data = {}
    for user in users:
        data[f"user{user.id}"] = user.to_dict()
    return jsonify(data)

<<<<<<< HEAD
=======
@api.route("/users",methods=["POST"])
def create_user():
    data = request.get_json()
    for field in ["username","email","password"]:
        if field not in data:
            return bad_request("Проверьте введенные данные!")
    if User.query.filter_by(username=data["username"]).first():
        return bad_request("Имя пользователя уже занято!")
    if User.query.filter_by(email=data["email"]).first():
        return bad_request("Почта уже занята!")
    u = User()
    u.from_dict(data)
    db.session.add(u)
    db.session.commit()
    response = jsonify(u.to_dict())
    response.status_code = 201
    return response
>>>>>>> b08e2d9fc7004f5c781600c8cef8dc8d0afe57a0

@api.route("/password/<string:name>", methods=["GET"])
@t_auth.login_required
def get_password(name):
<<<<<<< HEAD
    pass
=======
    user = User.query.filter_by(id=g.current_user.id).first()
    p = Password.query.filter_by(creator=user.id).first()
    if not p:
        return jsonify({"error":"no password found!"})
    return jsonify(p.to_dict())
>>>>>>> b08e2d9fc7004f5c781600c8cef8dc8d0afe57a0
