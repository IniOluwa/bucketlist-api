from . import db
from passlib.apps import custom_app_context as password_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app, g
from datetime import datetime


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    created_by = db.Column(db.String(64))

    def edit(self, new_name):
        self.name = new_name
        self.date_modified = datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(Base):
    __tablename__ = 'user'
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(64))
    user_bucketlists = db.relationship(
        'BucketList', backref=db.backref('bucketlist', lazy='joined'))

    def hash_password(self, password):
        self.password_hash = password_context.encrypt(password)

    def verify_password(self, password):
        return password_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id})

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

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'date_created': self.date_created
        }


class BucketList(Base):
    __tablename__ = 'bucketlist'
    name = db.Column(db.String(64), unique=True, index=True)
    items = db.relationship(
        'BucketListItem', backref=db.backref('bucketlistitem', lazy='joined'))
    date_modified = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_json(self):
        items = [item.to_json() for item in self.items]
        return {
            'id': self.id,
            'bucketlist': self.name,
            'items': items,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'user_id': self.user_id
        }


class BucketListItem(Base):
    __tablename__ = 'bucketlistitem'
    name = db.Column(db.String, unique=True, index=True)
    date_modified = db.Column(db.DateTime, default=datetime.now())
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'done': self.done
        }
