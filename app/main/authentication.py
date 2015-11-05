"""
File for user creation and authentication in app
"""
# Dependencies importation for authentication
from . import main
from ..models import User
from flask import request, jsonify, abort, url_for, g
from datetime import datetime
import jwt
import base64
from decorators import requires_auth


# User register route for new user creation
@main.route('/register', methods=['POST'])
def new_user():
    """New user creation"""
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
def get_user(id):
    """Getting users by id from database"""
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify(user.to_json())


# User login route for user login
@main.route('/auth/login', methods=['POST'])
def login_user():
    """logging in the user"""
    # getting json data from user
    username = request.json.get('username')
    password = request.json.get('password')
    # verifying user
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }

    payload = {
        "username": username,
        "password": password,
        "exp": "3600"
    }

    token = HMACSHA256(
        base64UrlEncode(header) + "." +
        base64UrlEncode(payload),
        secret
    )

    return jsonify({
        "user": username,
        "token": token,
        "status": "Logged in"
    })
    

    # else:
    #     return "Invalid username or password"


# User logout route for logging out user
@main.route('/auth/logout', methods=['GET'])
@requires_auth
def logout_user():
    """user logout"""
    return jsonify({
        'status': 'Logged out'
    })
