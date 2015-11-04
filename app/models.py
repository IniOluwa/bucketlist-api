"""
Database models for bucketlist API
"""
# Models dependencies imported
from . import db
from passlib.apps import custom_app_context as password_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app
from datetime import datetime


# Abstract base model class
class Base(db.Model):
    __abstract__ = True
    # id database column created
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    created_by = db.Column(db.String(64))

    # Method for editing database values
    def edit(self, new_name):
        self.name = new_name
        self.date_modified = datetime.now()

    # Method for saving values to the database
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Method for deleting values from the database
    def delete(self):
        db.session.delete(self)
        db.session.commit()


# User database model class
class User(Base):
    # User database tablename set as 'user'
    __tablename__ = 'user'
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(64))
    user_bucketlists = db.relationship(
        'BucketList', backref=db.backref('author', lazy='immediate'))

    # Method for hasing user password
    def hash_password(self, password):
        self.password_hash = password_context.encrypt(password)

    # Method for verifying hashed user password
    def verify_password(self, password):
        return password_context.verify(password, self.password_hash)

    # Method for generating user authentication token
    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id})

    # Static Method for User authentication token verification
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return User.query.get(data['id'])

    # Method for returning dictionary values of user data
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'date_created': self.date_created
        }


# Bucket list database model class
class BucketList(Base):
    # BacketList database tablename set as 'bucketlist'
    __tablename__ = 'bucketlist'
    name = db.Column(db.String(64), unique=True, index=True)
    items = db.relationship(
        'BucketListItem', backref=db.backref('bucketlist', lazy='immediate'))
    date_modified = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Method for returning dictionary values of bucketlist data
    def to_json(self):
        items = [item.to_json() for item in self.items]
        return {
            'id': self.id,
            'bucketlist': self.name,
            'items': items,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'owner': self.created_by
        }


# Bucket list item model class
class BucketListItem(Base):
    # BacketListItem database tablename set as 'bucketlistitem'
    __tablename__ = 'bucketlistitem'
    name = db.Column(db.String, unique=True, index=True)
    date_modified = db.Column(db.DateTime, default=datetime.now())
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))

    # Method for returning dictionary values of bucketlistitem data
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'done': False
        }
