#Embedded file name: C:\Users\Vince\Google Drive\PeacefulMandE\HelloWorldFlask\hello\models.py

from sqlalchemy import desc
from nimble import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

tags = db.Table('post_tag', 
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')), 
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')))

likes = db.Table('post_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')))

class Post(db.Model):
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
            self._tags = [ Tag.get_or_create(name) for name in string.split(',') ]
        else:
            self._tags = []

    def __repr__(self):
        return "content and url of post:"+\
        "'{}': '{}' || '{}'".format(self.content, self.url, self._tags)


class User(db.Model, UserMixin):
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
        return "<id|'{}' username : email '{}' : '{}'>".format(self.id, self.username, self.email)


class Tag(db.Model):
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
