# coding: utf8
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from datetime import datetime
from . import login_manager
from . import db

class User(UserMixin,db.Model):
    """用户的数据库模型
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.VARCHAR(64), unique = True, index=True)
    email =  db.Column(db.VARCHAR(64), unique = True)
    password_hash = db.Column(db.VARCHAR(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), server_default=('2'))
    firstname = db.Column(db.VARCHAR(20))
    phone = db.Column(db.Integer)
    active = db.Column(db.Boolean, nullable=False, server_default=('0'))
    lastname = db.Column(db.VARCHAR(20))
    update_time = db.Column(db.TIMESTAMP(True), onupdate = datetime.utcnow )
    create_time = db.Column(db.TIMESTAMP(True), nullable=False, default=datetime.utcnow)

    posts = db.relationship('Post',backref = 'author', lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.active = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username

    def test_no_password_getter(self):
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password = 'cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    role_name = db.Column(db.VARCHAR(64), unique = True)
    users = db.relationship('User', backref = 'role')

    def __repr__(self):
        return '<Role %r>' % self.role_name

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.TIMESTAMP, index=True, default = datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))


