"""
Configuration file
This file contains all app Configuration.
"""
import os
# Base directory path set
basedir = os.path.abspath(os.path.dirname(__file__))


# Basic app configurations
class Config:
    # App secret key set
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Inioluwa'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    BUCKETLIST_ADMIN = os.environ.get('BUCKETLIST_ADMIN')

    @staticmethod
    def init_app(app):
        pass


# Development configuration for app
class DevelopmentConfig(Config):
    DEBUG = True
    # Development database setting
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


# Testing configuration for app
class TestingConfig(Config):
    TESTING = True
    # Testing database setting
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


# Production deployment configuration for app
class ProductionConfig(Config):
    # Production database setting
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

# Configuration dictionary containing all app configurations
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
