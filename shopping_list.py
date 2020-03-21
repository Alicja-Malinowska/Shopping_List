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


def user_key(id):
    '''creates a user key to use as an ancestor for a list'''
    return ndb.Key('User', id)


class List(ndb.Model):
    '''Model to represent each list entity'''
    date = ndb.DateTimeProperty(auto_now_add=True)
    name = ndb.StringProperty()

class List_item(ndb.Model):
    '''Model to represent each item entity'''
    date = ndb.DateTimeProperty(auto_now_add=True)
    item = ndb.StringProperty(indexed=False)

class Home(webapp2.RequestHandler):
    '''Renders index.html for the homepage view'''
    def get(self):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url('/')
            linktext = 'Logout'
        else:
            url = users.create_login_url('/list.html')
            linktext = 'Login'
        
        values = {
            'url': url,
            'linktext': linktext
        }
        template = j_env.get_template('index.html')
        self.response.write(template.render(values))

class Dashboard(webapp2.RequestHandler):
    '''Handles the main view after login.
       Gets all the lists and all the items for the current
       list so they can be used in html to display them. 
       It also takes an information from URL if the list name
       that was attempted to add exists, if that is the case
       it creates a message that this name already exists. 
    '''
    def get(self):
        user = users.get_current_user()
        list_query = List.query(ancestor = user_key(user.user_id())).order(-List.date)
        lists = list_query.fetch()
        current_list_name = self.request.get('list')
        list_name_query = List.query(List.name == current_list_name, ancestor = user_key(user.user_id()))
        current_list = list_name_query.fetch()
        # if a list was selected get its items, otherwise no items should be displayed
        if len(current_list) > 0:
            item_query = List_item.query(ancestor = current_list[0].key).order(-List_item.date)
            items = item_query.fetch()
        else:
            items = []
        
        url = users.create_logout_url('/list.html')
        linktext = 'Logout'
        name_alert = ""
        item_alert = ""
        name_exists = self.request.get('exists')
        if name_exists == 'True':
            name_alert = "You already have a list with this name."
        #if no list chosen
        if current_list_name == "":
            item_alert = "Choose a list or create a new one to add items."
        values = {
            'nickname': user.nickname(),
            'url': url,
            'linktext': linktext,
            'list_items': items,
            'lists': lists,
            'list_name': current_list_name,
            'name_alert': name_alert,
            'item_alert': item_alert
        }
        template = j_env.get_template('list.html')
        self.response.write(template.render(values))
        

class AddList(webapp2.RequestHandler):
    ''' Adds a list only if a list of this name does not
    already exists in the database. Sends an information
    if the name already exists or not on the URL'''
    def post(self):
        user = users.get_current_user()
        list_query = List.query(ancestor = user_key(user.user_id())).order(-List.date)
        lists = list_query.fetch()
        current_list_name = self.request.get('list')
        exists = False
        # add a list only if a list with this name doesn't already exists
        for a_list in lists:
            if a_list.name == current_list_name:
                exists = True
                break
        if not exists:
            new_list = List(name = current_list_name, parent = user_key(user.user_id()))
            new_list.put()
               
        query_params = {'list': current_list_name, 'exists': exists}
        self.redirect('/list.html?' + urllib.urlencode(query_params))


class AddItem(webapp2.RequestHandler):
    ''' Adds an item to a specifi list. It does not add anything if 
    a list is not selected '''
    def post(self):
        user = users.get_current_user()
        current_list_name = self.request.get('list_name')
        list_query = List.query(List.name == current_list_name, ancestor = user_key(user.user_id()))
        current_list = list_query.fetch()
        if len(current_list) > 0:
            new_item = List_item(item = self.request.get('item'), parent = current_list[0].key)
            new_item.put()
        query_params = {'list': current_list_name}
        self.redirect('/list.html?' + urllib.urlencode(query_params))
            
class DeleteList(webapp2.RequestHandler):
    ''' Deletes a currently selected list together with all its items '''
    def post(self):
        user = users.get_current_user()
        current_list_name = self.request.get('list_name')   
        list_query = List.query(List.name == current_list_name, ancestor = user_key(user.user_id()))
        current_list = list_query.fetch()
        if len(current_list) > 0:
            items_query = List_item.query(ancestor = current_list[0].key)
            items = items_query.fetch()
            for item in items:
                item.key.delete()
            current_list[0].key.delete()
        self.redirect('/list.html')
        

class DeleteAll(webapp2.RequestHandler):
    ''' Deletes all the items from a selected list '''
    def post(self):
        user = users.get_current_user()
        current_list_name = self.request.get('list_name')
        list_query = List.query(List.name == current_list_name, ancestor = user_key(user.user_id()))
        current_list = list_query.fetch()
        if len(current_list) > 0:
            items_query = List_item.query(ancestor = current_list[0].key)
            list_items = items_query.fetch()
            for item in list_items:
                item.key.delete()
        query_params = {'list': current_list_name}
        self.redirect('/list.html?' + urllib.urlencode(query_params))
        

class DeleteItem(webapp2.RequestHandler):
    ''' Deletes a chosen item from a selected list.
        This happens by recreating the item key
        using its ID which was saved as a html element id'''
    def post(self):
        user = users.get_current_user()
        current_list_name = self.request.get('list_name')
        list_query = List.query(List.name == current_list_name, ancestor = user_key(user.user_id()))
        current_list = list_query.fetch()
        item_id = self.request.get('item_id')
        key = ndb.Key('User', str(user.user_id()), 'List', int(current_list[0].key.id()), 'List_item', int(item_id))
        key.delete()
        query_params = {'list': current_list_name}
        self.redirect('/list.html?' + urllib.urlencode(query_params))
        

class EditItem(webapp2.RequestHandler):
    ''' Allows to edit an existing item of the selected list.
        Recreates the item's key and then, using the key,
        gets the item and edits with the new value of input'''
    def post(self):
        user = users.get_current_user()
        current_list_name = self.request.get('list_name')
        list_query = List.query(List.name == current_list_name, ancestor = user_key(user.user_id()))
        current_list = list_query.fetch()
        item_id = self.request.get('item_id')
        edited_item = self.request.get('edit_item')
        key = ndb.Key('User', str(user.user_id()), 'List', int(current_list[0].key.id()), 'List_item', int(item_id))
        item = key.get()
        item.item = edited_item
        item.put()
        query_params = {'list': current_list_name}
        self.redirect('/list.html?' + urllib.urlencode(query_params))


app = webapp2.WSGIApplication([
    ('/', Home),
    ('/list.html', Dashboard),
    ('/list.html/add-list', AddList),
    ('/list.html/add', AddItem),
    ('/list.html/delete-all', DeleteAll),
    ('/list.html/delete', DeleteItem),
    ('/list.html/edit', EditItem),
    ('/list.html/delete-list', DeleteList)
])