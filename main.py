#! /usr/bin/env python

# dev_appserver.py /home/vince/TZU/UD/nimble/default

# to switch on the app on, has funcs to reset the db

import logging
from nimble import *
from nimble.models import *
from flask_script import Manager

if __name__ == '__main__':
    mgmt.run()