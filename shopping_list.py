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


def user_key(id):
    return ndb.Key('User', id)

class List(ndb.Model):
     user_id = ndb.StringProperty()
     date = ndb.DateTimeProperty(auto_now_add=True)
     name = ndb.StringProperty()

class List_item(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    item = ndb.StringProperty(indexed=False)

class Home(webapp2.RequestHandler):
    def get(self):
        
        template = j_env.get_template('index.html')
        self.response.write(template.render())

class NewList(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        list_query = List.query(List.user_id == user.user_id(), ancestor = user_key(user.user_id())).order(-List.date)
        lists = list_query.fetch()
        list_name = self.request.get('list')
        list_name_query = List.query(List.user_id == user.user_id(), List.name == list_name, ancestor = user_key(user.user_id()))
        the_list = list_name_query.fetch()
        if len(the_list) > 0:
            item_query = List_item.query(ancestor = the_list[0].key).order(-List_item.date)
            list_items = item_query.fetch()
        else:
            list_items = []
        url = users.create_logout_url('/list.html')
        linktext = 'Logout'
        alert = ""
        name_exists = self.request.get('exists')
        if name_exists == 'True':
            alert = "You already have a list with this name."
        values = {
            'nickname': user.nickname(),
            'url': url,
            'linktext': linktext,
            'list_items': list_items,
            'lists': lists,
            'list_name': list_name,
            'alert': alert
        }
        template = j_env.get_template('list.html')
        self.response.write(template.render(values))
        #self.response.write(name_exists)

class AddList(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        list_query = List.query(List.user_id == user.user_id(), ancestor = user_key(user.user_id())).order(-List.date)
        lists = list_query.fetch()
        list_name = self.request.get('list')
        exists = False
        for a_list in lists:
            if a_list.name == list_name:
                exists = True
                break
        if not exists:
            new_list = List(user_id = user.user_id(), name = list_name, parent = user_key(user.user_id()))
            new_list.put()
               
        query_params = {'list': list_name, 'exists': exists}
        self.redirect('/list.html?' + urllib.urlencode(query_params))


class AddItem(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        list_name = self.request.get('list_name')
        list_query = List.query(List.user_id == user.user_id(), List.name == list_name, ancestor = user_key(user.user_id()))
        the_list = list_query.fetch()
        new_item = List_item(item = self.request.get('item'), parent = the_list[0].key)
        new_item.put()
        query_params = {'list': list_name}
        self.redirect('/list.html?' + urllib.urlencode(query_params))
        
        
        

class DeleteAll(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        list_name = self.request.get('list_name')
        list_query = List.query(List.user_id == user.user_id(), List.name == list_name, ancestor = user_key(user.user_id()))
        the_list = list_query.fetch()
        items_query = List_item.query(ancestor = the_list[0].key)
        list_items = items_query.fetch()
        for item in list_items:
            item.key.delete()
        query_params = {'list': list_name}
        self.redirect('/list.html?' + urllib.urlencode(query_params))
        #self.response.write(list_items[0].key)

class DeleteItem(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        list_name = self.request.get('list_name')
        list_query = List.query(List.user_id == user.user_id(), List.name == list_name, ancestor = user_key(user.user_id()))
        the_list = list_query.fetch()
        item_id = self.request.get('item_id')
        key = ndb.Key('User', str(user.user_id()), 'List', int(the_list[0].key.id()), 'List_item', int(item_id))
        key.delete()
        query_params = {'list': list_name}
        self.redirect('/list.html?' + urllib.urlencode(query_params))
        

class Edit(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        list_name = self.request.get('list_name')
        list_query = List.query(List.user_id == user.user_id(), List.name == list_name, ancestor = user_key(user.user_id()))
        the_list = list_query.fetch()
        item_id = self.request.get('item_id')
        edited = self.request.get('edit_item')
        key = ndb.Key('User', str(user.user_id()), 'List', int(the_list[0].key.id()), 'List_item', int(item_id))
        list_item = key.get()
        list_item.item = edited
        list_item.put()
        query_params = {'list': list_name}
        self.redirect('/list.html?' + urllib.urlencode(query_params))


app = webapp2.WSGIApplication([
    ('/', Home),
    ('/list.html', NewList),
    ('/list.html/add-list', AddList),
    ('/list.html/add', AddItem),
    ('/list.html/delete-all', DeleteAll),
    ('/list.html/delete', DeleteItem),
    ('/list.html/edit', Edit)
    
], debug=True)# remember to remove!!!!!!!!!!!