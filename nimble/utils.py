"""utils.py contains various utility functions for generating configurations.

These functions are used around the app, mostly in views.py and models.py. sa

The primary needs are setting global configurations and generating hashes
and other useful reused outputs.

"""
import random
import string
import hashlib
import time

from flask import redirect, current_app, make_response, request, url_for, session
from functools import wraps

from nimble import app, ghost_user
from models import User


def make_pw_hash_salt(name, pw):
    '''This generates a hash and a random salt, returning both in a tuple.

    The salt is not argument dependent and will only be availible where 
    the hash is as well.

    The hash is created from the name, password argument, and the salt.
    '''
    name = str(name)
    pw = str(pw)
    salt = ''.join(random.choice(string.letters) for x in xrange(15))
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)


def login_cookie_bake(user):
    '''Adds tuple of username and a new login hash to 
    a session configuration embeded in flask.
    see - http://flask.pocoo.org/docs/0.12/quickstart/#session

    While the hash stored in the user database object is used in the original
    authentication, a new hash and username combo is generated and used to
    validate the session through a server side configuration (session)

    The user argument should be a valid instance of the user model

    '''
    secret = user.password_hash[2:5]
    session_hash_str = hashlib.sha256(secret).hexdigest()
    print 'sess id from req'
    print request.cookies
    app.config['current_user'] = user
    session['user'] = (str(user.username),session_hash_str)


def is_logged_in(): 
    '''Immediately prints the session and checks if the user is logged in.
    Returns the corresponding boolean.

    A user object is retrieved from the database and checked against the 
    'ghost', and then a hash is generated using the same string as the login 
    hash as a second layer of security.

    '''
    if 'user' in session.keys():
        print "app.config['current_user']"
        print app.config['current_user']
        print 'session'
        print session
        query_user = User.gql("WHERE username = :u", u = session['user'][0]).get()
        if query_user:
            if query_user != ghost_user and\
                session['user'][1] == \
                    hashlib.sha256(query_user.password_hash[2:5]).hexdigest():
                return True
            else:
                return False
    else:
        return False


def get_current_user():
    '''Returns a user object. 

    If is_logged_in (function just above this) returns true, the user object
    set in login_cookie_bake above is returned.

    '''
    if is_logged_in():
        return app.config['current_user']
    else:
        return ghost_user


def logout_user():
    '''Standard logout function
    The session config is restored to the pre-login state, and the ghost user
    is set back to its value in __init__
    '''
    app.config['current_user'] = ghost_user
    session['user'] = None


def login_required(func):
    '''simplified version of decorator from flask login - utils.py.
    see
    flask-login.readthedocs.io/en/latest/#flask_login.login_required

    This function wrapper takes a function and runs is_logged_in, 
    returning the view as normal if True and redirecting to the login page if
    false.

    '''
    @wraps(func)
    def decorated_view(*args, **kwargs):
        print 'session'
        print session
        if not is_logged_in():
            print 'at url for'
            print func
            print 'login req - user not logged in.'
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_view