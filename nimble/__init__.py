"""Welcome to the Nimble blog code base. Using a SQLlite, this app works as a 
text only micro blog. It is designed for simplicity and anonymity.

This is a standard flask init file which sets up database 
and login configurations"""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy, SignallingSession
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +\
os.path.join(basedir, 'nimble.db')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'to_start'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
toolbar = DebugToolbarExtension(app)

import models
from models import *
import views
from views import *
