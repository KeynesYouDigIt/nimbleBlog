import random
import string
import hashlib
import time

from flask import redirect, current_app, make_response, request, url_for, session
from functools import wraps

from nimble import app, ghost_user
from models import User

def make_pw_hash_salt(name, pw):
    salt = ''.join(random.choice(string.letters) for x in xrange(15))
    print salt
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)


def login_cookie_bake(user):
    '''adds tuple of username and hash to session configuration embeded in flask

    http://flask.pocoo.org/docs/0.12/quickstart/#session
    '''
    secret = user.password_hash[2:5]
    session_hash_str = hashlib.sha256(secret).hexdigest()
    print 'sess id from req'
    print request.cookies
    app.config['current_user'] = user
    session['user'] = (str(user.username),session_hash_str)

def is_logged_in():
    if 'user' in session.keys():
        print "app.config['current_user']"
        print app.config['current_user']
        query_user = User.gql("WHERE username = :u", u = session['user'][0]).get()
        if query_user != ghost_user and\
            session['user'][1] == \
                hashlib.sha256(query_user.password_hash[2:5]).hexdigest():
            print 'user auth!'
            return True
        else:
            return False
    else:
        return False


def get_current_user():
    if is_logged_in():
        return app.config['current_user']
    else:
        return ghost_user

def logout_user():
    app.config['current_user'] = ghost_user
    session['user'] = None


def login_required(func):
    '''simplified version of util from flask login - utils.py'''
    @wraps(func)
    def decorated_view(*args, **kwargs):
        print 'session'
        print session
        if not is_logged_in():
            print 'login req - user not auth'
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_view
