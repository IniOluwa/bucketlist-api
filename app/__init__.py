"""
Python package file making it's current directory a python package
"""
# Package dependecies importation
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

# SQLAlchemy set as primary database
db = SQLAlchemy()


# Method for creation of new flask app
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize SQLAlchemy database with flask app
    db.init_app(app)


    # Flask blueprint importation and initialization for app
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Return flask app for execution
    return app
