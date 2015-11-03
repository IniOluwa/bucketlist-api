from . import main
from ..models import User
from ..import db
from flask import request, jsonify, abort, url_for, g, session
from datetime import datetime
from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


# New user creation
@main.route('/register', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        # Missing arguements
        abort(400)
    if User.query.filter_by(username=username).first() is not None:
        # User already exists
        abort(400)
    user = User(username=username)
    user.hash_password(password)
    user.date_created = datetime.now()
    db.session.add(user)
    db.session.commit()
    return jsonify(
        {
            'username': user.username,
            'Location': url_for('main.login_user', _external=True)
        }), 201


# get user
@main.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify(user.to_json())


# user login
@main.route('/auth/login', methods=['POST'])
def login_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if verify_password(username, password):
        user = User.query.filter_by(username=username).first()
        token = user.generate_auth_toszken(3600)
        return jsonify({
            'user': username,
            'token': token.decode('ascii'),
            'status': 'Logged in'
            }), 201
    else:
        return "Invalid username or password"


# user logout
@main.route('/auth/logout', methods=['GET'])
@auth.login_required
def logout_user():
    return jsonify({
        'status': 'Logged out'
    })


# password and token authentication
@auth.verify_password
def verify_password(username_or_token, password):
    # authentication by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True
