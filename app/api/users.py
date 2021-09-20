from app.api import api
from app.models import User
from flask import jsonify

@api.route("/users/<int:id>",methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@api.route("/users",methods=['GET'])
def get_users():
    users = User.query.all()
    data = {}
    for user in users:
        data[f"user{user.id}"] = user.to_dict()
    return jsonify(data)

@api.route("/users",methods=["POST"])
def create_user():
    pass