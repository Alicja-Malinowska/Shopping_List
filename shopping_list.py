import os
import json
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




def user_key(nickname):
    return ndb.Key('User', nickname)

class List_item(ndb.Model):
    user_id = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    item = ndb.StringProperty(indexed=False)

class Home(webapp2.RequestHandler):
    def get(self):
        
        template = j_env.get_template('index.html')
        self.response.write(template.render())

class NewList(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        list_query = List_item.query(List_item.user_id == user.user_id(), ancestor = list_key()).order(-List_item.date)
        list_items = list_query.fetch()
        url = users.create_logout_url(self.request.uri)
        linktext = 'Logout'
        values = {
            'nickname': user.nickname(),
            'url': url,
            'linktext': linktext,
            'list_items': list_items
        }
        template = j_env.get_template('list.html')
        self.response.write(template.render(values))

class Add(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        new_item = List_item(user_id = user.user_id(), item = self.request.get('item'), parent = list_key())
        new_item.put()
        self.redirect('/list.html')

class DeleteAll(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        list_query = List_item.query(List_item.user_id == user.user_id(), ancestor = list_key()).order(-List_item.date)
        list_items = list_query.fetch()
        for item in list_items:
            item.key.delete()
        self.redirect('/list.html')

class DeleteItem(webapp2.RequestHandler):
    def post(self):
        item_id = self.request.get('item_id')
        key = ndb.Key('Shopping List', 'List', 'List_item', int(item_id))
        key.delete()
        self.redirect('/list.html')

class Edit(webapp2.RequestHandler):
    def post(self):
        item_id = self.request.get('item_id')
        edited = self.request.get('edit_item')
        key = ndb.Key('Shopping List', 'List', 'List_item', int(item_id))
        list_item = key.get()
        list_item.item = edited
        list_item.put()
        self.redirect('/list.html')


app = webapp2.WSGIApplication([
    ('/', Home),
    ('/list.html', NewList),
    ('/list.html/add', Add),
    ('/list.html/delete-all', DeleteAll),
    ('/list.html/delete', DeleteItem),
    ('/list.html/edit', Edit)
    
], debug=True)# remember to remove!!!!!!!!!!!