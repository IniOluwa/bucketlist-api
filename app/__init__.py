from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from main import main as main_blueprint

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app()

    db.init_app(app)
    app.register_blueprint(main_blueprint)

    # attach routes and custom error pages here and it will be initialized along with the Flask app when running the server.

    return app
