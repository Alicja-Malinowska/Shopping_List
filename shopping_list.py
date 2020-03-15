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

DAFAULT_LIST_NAME = 'List'


def list_key(name = DAFAULT_LIST_NAME):
    return ndb.Key('Shopping List', name)

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
        list_name = self.request.get('list_name', DAFAULT_LIST_NAME)
        user = users.get_current_user()
        list_query = List_item.query(List_item.user_id == user.user_id(), ancestor = list_key(list_name)).order(-List_item.date)
        list_items = list_query.fetch()
        url = users.create_logout_url(self.request.uri)
        linktext = 'Logout'
        values = {
            'nickname': user.nickname(),
            'url': url,
            'linktext': linktext,
            'list_items': list_items,
            'list_name': list_name
        }
        template = j_env.get_template('list.html')
        self.response.write(template.render(values))

class Add(webapp2.RequestHandler):
    def post(self):
        list_name = self.request.get('list_name', DAFAULT_LIST_NAME)
        user = users.get_current_user()
        new_item = List_item(user_id = user.user_id(), item = self.request.get('item'), parent = list_key(list_name))
        new_item.put()
        query_params = {'list_name': list_name}
        self.redirect('/list.html?' + urllib.urlencode(query_params))
        

class DeleteAll(webapp2.RequestHandler):
    def post(self):
        list_name = self.request.get('list_name', DAFAULT_LIST_NAME)
        user = users.get_current_user()
        list_query = List_item.query(List_item.user_id == user.user_id(), ancestor = list_key(list_name)).order(-List_item.date)
        list_items = list_query.fetch()
        for item in list_items:
            item.key.delete()
        query_params = {'list_name': list_name}
        self.redirect('/list.html?' + urllib.urlencode(query_params))

class DeleteItem(webapp2.RequestHandler):
    def post(self):
        list_name = self.request.get('list_name', DAFAULT_LIST_NAME)
        item_id = self.request.get('item_id')
        key = ndb.Key('Shopping List', list_name, 'List_item', int(item_id))
        key.delete()
        query_params = {'list_name': list_name}
        self.redirect('/list.html?' + urllib.urlencode(query_params))

class Edit(webapp2.RequestHandler):
    def post(self):
        list_name = self.request.get('list_name', DAFAULT_LIST_NAME)
        item_id = self.request.get('item_id')
        edited = self.request.get('edit_item')
        key = ndb.Key('Shopping List', list_name, 'List_item', int(item_id))
        list_item = key.get()
        list_item.item = edited
        list_item.put()
        query_params = {'list_name': list_name}
        self.redirect('/list.html?' + urllib.urlencode(query_params))


app = webapp2.WSGIApplication([
    ('/', Home),
    ('/list.html', NewList),
    ('/list.html/add', Add),
    ('/list.html/delete-all', DeleteAll),
    ('/list.html/delete', DeleteItem),
    ('/list.html/edit', Edit)
    
], debug=True)# remember to remove!!!!!!!!!!!