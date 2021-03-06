from . import db, login
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):
    """User"""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140), unique=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship('User', secondary=followers, primaryjoin=(followers.c.follower_id == id), secondaryjoin=(followers.c.followed_id == id),
     backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_check(self, password):
        return check_password_hash(self.password_hash, password)

    # @property
    # def password(self):
    #     raise ValueError('Can not read passwords.')
    #
    # @property.setter
    # def password(self, value):
    #     self.password_hash = generate_password_hash(value)

    @property
    def is_admin(self):
        return current_app.config['ADMIN_EMAIL'] == self.email

    @is_admin.setter
    def is_admin(self, value):
        raise ValueError('is_admin not settable.')

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):

    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    done = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return '<Post {}>'.format(self.body)
