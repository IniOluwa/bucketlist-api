"""
Token authentication decorator
"""
# Importation of dependencies for toking decoding
import jwt
import os

from functools import wraps
from flask import Flask, request, jsonify, _request_ctx_stack, current_app


# Error method for authentication
def authenticate(error):
    resp = jsonify(error)
    resp.status_code = 401
    return resp


def requires_authentication(f):
    """Creation of authentication decorator"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Getting request headers
        auth = request.headers.get('Authorization', None)
        if not auth:
          return authenticate({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'})

        # Splitting of headers information
        parts = auth.split()

        # Validation of headers information
        if len(parts) == 1:
          return {'code': 'invalid_header', 'description': 'Token not found'}
        elif len(parts) > 2:
          return {'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}

        # Separating of 'token from headers information'
        token = parts[1]
        try:
            # Decoding of token
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithm='HS256')
        except jwt.ExpiredSignature:
            return authenticate({'code': 'token_expired', 'description': 'token is expired'})
        except jwt.InvalidAudienceError:
            return authenticate({'code': 'invalid_audience', 'description': 'incorrect audience, expected: YOUR_CLIENT_ID'})
        except jwt.DecodeError:
            return authenticate({'code': 'token_invalid_signature', 'description': 'token signature is invalid'})

        # Return of decoded data
        _request_ctx_stack.top.current_user = user = payload
        return f(*args, **kwargs)

    return decorated