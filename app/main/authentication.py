"""
File for user creation and authentication in app
"""
# Dependencies importation for authentication
from . import main
from ..models import User
from flask import request, jsonify, abort, url_for, g
from datetime import datetime
from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


# User register route for new user creation
@main.route('/register', methods=['POST'])
# New user creation
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        # if username or password is missing
        abort(400)
    if User.query.filter_by(username=username).first() is not None:
        # if user already exists
        abort(400)
    # Creating new user
    user = User(username=username)
    user.hash_password(password)
    user.date_created = datetime.now()
    # Saving new user
    user.save()
    # Returning new user and login url
    return jsonify(
        {
            'username': user.username,
            'Location': url_for('main.login_user', _external=True)
        }), 201


# Get users route for getting users
@main.route('/users/<int:id>', methods=['GET'])
# get registered users
def get_user(id):
    # getting users by id from database
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify(user.to_json())


# User login route for user login
@main.route('/auth/login', methods=['POST'])
# user login
def login_user():
    # getting json data from user
    username = request.json.get('username')
    password = request.json.get('password')
    # verifying user
    if verify_password(username, password):
        user = User.query.filter_by(username=username).first()
        token = user.generate_auth_token(3600)
        # returning a token to the user for authorization for an hour
        return jsonify({
            'user': username,
            'token': token.decode('ascii'),
            'status': 'Logged in'
            }), 201
    else:
        return "Invalid username or password"


# User logout route for logging out user
@main.route('/auth/logout', methods=['GET'])
# user logout
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
