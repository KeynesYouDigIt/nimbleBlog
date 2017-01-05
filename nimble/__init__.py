"""Welcome to the Nimble blog code base. Using a SQLlite, this app works as a 
text only micro blog. It is designed for simplicity and anonymity.

This is a standard flask init file which sets up database 
and login configurations"""

import os

from flask import Flask
from google.appengine.ext import db

from flask_debugtoolbar import DebugToolbarExtension

db = db

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

Flask.current_app = app

app.config['SECRET_KEY'] = os.urandom(35)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +\
os.path.join(basedir, 'nimble.db')
    
toolbar = DebugToolbarExtension(app)

from models import *

# a ghost user is created since the login validation and some user lookup 
# methods need a user to work at all. the "ghost" is logged in, 
# but does not have a session hash string, allowing explicit testing of
# login status.

ghost_user = User.gql("WHERE  username = :username", username = '83928482956').get()
print 'ghost user get'
print ghost_user

if not ghost_user:
    ghost_user = User(email = 'ghost@ghost.org',
                    username = '83928482956',
                    password_hash = '__')
    ghost_user.put()
    ghost_user = User.gql(\
        "WHERE  username = :username", username = '83928482956').get()
    print '! ghost_user added'

app.config['current_user'] = ghost_user
print 'ghost user set'
print 'dir app'
print dir(app.app_context())

from views import *