"""Welcome to the Nimble blog code base. Using a google db data store, 
this app works as a text only micro blog. 

It is designed for simplicity and anonymity.

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
app.config['DEBUG'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +\
os.path.join(basedir, 'nimble.db')
    
toolbar = DebugToolbarExtension(app)

from models import *

# Flask-Login created significant compadibility issues,
# and session management is part o the curriculum for this course, so the
# below is an attempt at that.

# To start any session pre log in,
# a ghost user is created. the "ghost" is logged in, 
# but does not have a session hash string and has a specific string of numbers
# for a username. This makes login validation explicit and straight forward.

ghost_user = User.gql("WHERE  username = :username", username = '83928482956').get()
print 'ghost user get'
print ghost_user

if not ghost_user:
	# if the ghost user doesnt exist yet, this is the first time the app is 
	# being run on a particular deployment.
	# The ghost is therefore created.

    ghost_user = User(email = 'ghost@ghost.org',
                    username = '83928482956',
                    password_hash = '__')
    ghost_user.put()
    ghost_user = User.gql(\
        "WHERE  username = :username", username = '83928482956').get()
    print '! ghost_user added'

# app.config is the global config enviroment for flask - 
# assign ghost_user to current
app.config['current_user'] = ghost_user
print 'ghost user set'

from views import *