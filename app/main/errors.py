"""
Bucketlist API error handling
"""
from flask import jsonify, make_response
from . import main


# Error handler for bad requests
@main.errorhandler(400)
def bad_request(e):
    """
    Method for bad request error
    """
    return make_response(
        jsonify({'error': 'Bad Request'}), 400
    )


# Error handler for unauthorized requests
@main.errorhandler(401)
def unauthorized(e):
    """
    Method for bad request error
    """
    return make_response(
        jsonify({'error': 'Unauthorized'}), 401
    )


# Error handler for routes not found
@main.errorhandler(404)
def not_found(e):
    """
    Method for bad request error
    """
    return make_response(
        jsonify({'error': 'Not found'}), 404
    )
