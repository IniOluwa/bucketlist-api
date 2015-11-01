from . import db
from datetime import datetime
# from os import os
# from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy

# basedir = os.path.abspath(os.path.dirname(__file__))

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] =\
#     'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# db = SQLAlchemy(app)


class Base(db.Models):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(default=datetime.utcnow())


class User(Base):
    __tablename__ = 'user'
    username = db.Column(db.String(64), unique=True, index=True)
    # password =
    user_bucketlists = db.relationship('BucketList', lazy='immediate')

    def __repr__(self):
        return '<User %r>' % self.username


class BucketList(Base):
    __tablename__ = 'bucketlist'
    name = db.Column(db.String(64), unique=True, index=True)
    items = db.relationship('BucketListItem', lazy='immediate')
    date_modified = db.Column(default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<BucketList %r>' % self.name


class BucketListItem(Base):
    __tablename__ = 'bucketlistitem'
    name = db.Column(db.String, unique=True, index=True)
    date_modified = db.Column(default=datetime.utcnow())
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))

    def __repr__(self):
        return '<BucketListItem %r>' % self.name
