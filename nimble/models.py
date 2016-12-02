"""This file creates models, 
which are passed to the router in views.py to take form data and store it.

configurations are in init.py and initial tasks for setup are in db_switch.py"""
from sqlalchemy import desc
from nimble import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

"""these first 2 tables are created for many to many relationships between 
posts and tags as well ass users that like posts and posts"""

tags = db.Table('post_tag', 
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')), 
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')))

likes = db.Table('post_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')))

class Post(db.Model):
    """This model allows post storage.

    id is an auto incrementing primary key

    url will be like the name of the post with a '/' added for easy routing
    and a web aesthetic when displayed.

    content is an open text field containing the content of the post 
    with no restrictions.

    u_t_id links Users to posts

    _tags links tags to posts

    _liked stores a list of Users that have liked a post
    """
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=True)
    u_t_id = db.Column(db.Integer, 
        db.ForeignKey('user.id'), 
        nullable = False)
    _tags = db.relationship('Tag', 
        secondary = tags, 
        lazy = 'joined', 
        backref = db.backref('psts', lazy='dynamic'))
    _liked = db.relationship('User',
        secondary=likes,
        lazy='joined',
        backref = db.backref('likes', lazy='dynamic'))

    @staticmethod
    def newest(num):
        return post.query.order_by(desc(post.date)).limit(num)

    @staticmethod
    def get_newest(num):
        return post.query.order_by(desc(post.id)).limit(num)

    @property
    def tags(self):
        return ','.join([ t.name for t in self._tags ])

    @tags.setter
    def tags(self, string):
        if string:
            self._tags = [Tag.get_or_create(name) for name in string.split(',')]
        else:
            self._tags = []

    def __repr__(self):
        return "content and url of post:"+\
        "'{}': '{}' || '{}'".format(self.content, self.url, self._tags)


class User(db.Model, UserMixin):
    """This model allows user storage.

    id is an auto incrementing primary key

    username is a username, must be provided and unique

    email is email, does not have to be unique

    posts stores posts by the user

    password_hash is the encrypted storage of the user password
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=False)
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return "<id|'{}' username : email '{}' : '{}'>".format(\
            self.id, self.username, self.email)


class Tag(db.Model):
    """This model allows tag storage.

    id is an auto incrementing primary key

    name is the tag as a string
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True, index=True)

    @staticmethod
    def get_or_create(name):
        try:
            return Tag.query.filter_by(name=name).one()
        except:
            return Tag(name=name)

    @staticmethod
    def all():
        return Tag.query.all()

    def __repr__(self):
        return "<id|'{}', tag string|'{}'>".format(self.id, self.name)
