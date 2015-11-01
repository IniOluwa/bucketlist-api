from . import db
from passlib.apps import custom_app_context as password_context
from datetime import datetime


class Base(db.Models):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.now())


class User(Base):
    __tablename__ = 'user'
    username = db.Column(db.String(64), unique=True, index=True)
    user_password = db.Column(db.String(64))
    user_bucketlists = db.relationship('BucketList', lazy='immediate')

    def hash_password(self, password):
        self.user_password = password_context.encrypt(password)

    def verify_password(self, password):
        return password_context(password, self.user_password)

    def __repr__(self):
        return '<User %r>' % self.username


class BucketList(Base):
    __tablename__ = 'bucketlist'
    name = db.Column(db.String(64), unique=True, index=True)
    items = db.relationship('BucketListItem', lazy='immediate')
    date_modified = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<BucketList %r>' % self.name


class BucketListItem(Base):
    __tablename__ = 'bucketlistitem'
    name = db.Column(db.String, unique=True, index=True)
    date_modified = db.Column(db.DateTime, datetime.now())
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))

    def __repr__(self):
        return '<BucketListItem %r>' % self.name
