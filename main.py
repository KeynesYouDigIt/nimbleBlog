#! /usr/bin/env python

#switch on the app on, has funcs to reset the db

import logging
from nimble import *
from nimble.models import *
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.exc import IntegrityError

mgmt = Manager(app)
migrate = Migrate(app, db)

mgmt.add_command('db', MigrateCommand)
# run python db_switch.py db migrate -m "message"
#and
# python db_switch.py db upgrade -m "message"
#to migrate this sucker base on changes made to models.py

@mgmt.command
def make_examples(with_examples=True):
    db.create_all()
    if with_examples==True:
        '''add user examples king arthur and sir lancelot'''
        Lance = User(username='Sir Lancelot', email='HolyHandGrenade15@camelot.org',password='camelot')
        db.session.add(Lance)
        Arthr = User(username='King Arthur', email='KingA@camelot.org',password='camelot')
        db.session.add(Arthr)
        db.session.commit()
        '''add tags'''
        pwnd=Tag(name="pwnd")
        db.session.add(pwnd)
        hist=Tag(name="history")
        db.session.add(hist)
        db.session.commit()
        
        '''add bookmarks'''
        blackknight = Post(url="/black_knight", 
            content = "I pwned the black knight like a bau5, thats all you need to know.", 
            user = Arthr, 
            _tags = [pwnd,hist],
            _liked = [Lance])
        
        db.session.add(blackknight)
        
        mystory=Post(url="/mystory",
            content = "Lancelot was super baller all his life thats my whole history yay", 
            user = Lance, 
            _tags = [hist])
        db.session.add(mystory)
        db.session.commit()
    print 'Database Initialized'

@mgmt.command
def drop_db():
    if prompt_bool("Are you sure you would like to permanently erase this data? MAKE SURE YOU DO ANOTHER upgrade AFTER THIS. STUPID."):
        db.drop_all()
        print "dropped db"

if __name__ == '__main__':
    mgmt.run()