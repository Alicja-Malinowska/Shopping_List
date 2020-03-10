import os

import urllib
#import users API to use for login and authentication
from google.appengine.api import users
#import ndb to be able to use datastore
from google.appengine.ext import ndb
#import jinja2 for templating
import jinja2
#import webapp2 to handle http requests
import webapp2

#create jinja2 environment to enable loading templates
j_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Home(webapp2.RequestHandler):
    def get(self):
        
        template = j_env.get_template('index.html')
        self.response.write(template.render())

class NewList(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            template = j_env.get_template('list.html')
            self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', Home),
    ('/list.html', NewList)
], debug=True)