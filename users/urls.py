from flask import abort, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..app import app
from .. import db, jwt
from .models import User


@app.route('/users/register', methods=['POST'])
def register():
    request_form = request.form.to_dict()
    username = request_form['username']
    password = request_form['password']
    if username is None or password is None:
        abort(400)
    if User.query.filter_by(username = username).first() is not None:
        abort(400)
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@app.route("/users/login", methods=["POST"])
def login():
    request_form = request.form.to_dict()
    username = request_form['username']
    password = request_form['password']

    user = User.query.filter_by(username=username).one_or_none()
    if not user or not user.verify_password(password):
        return jsonify("Wrong username or password"), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)


@app.route("/users/<user_id>", methods=["POST"])
@jwt_required()
def update(user_id):
    user = User.query.get_or_404(user_id)
    user_jwt = get_jwt_identity()
    if user.id != user_jwt.id:
        return jsonify("Wrong username or password"), 401
    request_form = request.form.to_dict()
    username = request_form['username']
    password = request_form['password']
    if username is not None:
        user.username = username
    if password is not None:
        user.username = username
    response = User.query.get_or_404(user_id).toDict()
    return jsonify(response)


@app.route("/users/<user_id>", methods=["POST"])
@jwt_required()
def delete(user_id):
    user = User.query.get_or_404(user_id)
    user_jwt = get_jwt_identity()
    if user.id != user_jwt.id:
        return jsonify("Wrong username or password"), 401
    user.delete()
    db.session.commit()
    return ('Account with Id "{}" deleted successfully!').format(note_id)
