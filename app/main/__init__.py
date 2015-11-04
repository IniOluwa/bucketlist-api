"""
Python package file making it's current directory a python package
"""

# flask Blueprint imported enabling flask app to use blueprint
from flask import Blueprint

# Creation of 'main' as flask blueprint
main = Blueprint('main', __name__)

# Importation of files to work closely with blueprint
from . import views, errors, authentication
