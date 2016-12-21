"""`appengine_config` gets loaded when starting a new application instance."""

print 'running app  config yaya!'

from google.appengine.ext import vendor
# import vendor
# insert `lib` as a site directory so our `main` module can load
# third-party libraries, and override built-ins with newer
# versions.
try:
    vendor.add('nibmle\lib')
except as err:
    print err
