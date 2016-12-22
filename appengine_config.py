"""`appengine_config` gets loaded when starting a new application instance."""


# import sys
# import os.path

# # add `lib` subdirectory to `sys.path`, so our `main` module can load
# # third-party libraries.
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'nibmle\lib'))

print 'running app  config yaya!'

from google.appengine.ext import vendor
# import os
# import sys

# import vendor
# insert `lib` as a site directory so our `main` module can load
# third-party libraries, and override built-ins with newer
# versions.

# sys.path.insert(0,'./lib')
# print sys.path

from google.appengine.ext import vendor
print dir(vendor)
vendor.add('lib')
print 'I am the line after adding lib, it should have worked'