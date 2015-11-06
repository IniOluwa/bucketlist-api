"""
File for user creation and authentication in app
"""
# Dependencies importation for authentication
from . import main
from ..models import User
from flask import request, jsonify, abort, url_for, g, current_app
from datetime import datetime
from decor import requires_authentication


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
@requires_authentication
def get_user(id):
    """Getting users by id from database"""
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify(user.to_json())


# User login route for user login
@main.route('/auth/login', methods=['POST'])
@requires_authentication
def login_user():
    """logging in the user"""
    # getting json data from user
    username = request.json.get('username')
    password = request.json.get('password')


    if username is None or password is None:
        abort(400) 

    user = User.query.filter_by(username=username).first()
    if user is not None and user.verify_password(password):
        token = user.generate_auth_token()
        g.user = user
        response = {
            "token": token
        }
        return jsonify(response)
    else:
        abort(401)

# User logout route for logging out user
@main.route('/auth/logout', methods=['GET'])
@requires_authentication
def logout_user():
    """user logout"""
    return jsonify({
        'status': 'Logged out'
    })
