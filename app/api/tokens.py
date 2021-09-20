from flask import jsonify,g
from app import db
from app.api import api
from app.api.auth import b_auth,t_auth

@api.route("/tokens",methods=["POST"])
@b_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({"token":token})


@api.route('/tokens',methods=["DELETE"])
@t_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return "",204