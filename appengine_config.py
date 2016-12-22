"""`appengine_config` gets loaded when starting a new application instance."""

print 'running app  config yaya!'

import vendor
vendor.add('lib')
print 'I am the line after adding lib, it should have worked'
import os
print os.getcwd()