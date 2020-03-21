# [ShopIt](https://shopping-list-270708.appspot.com/) - a shopping list app

This is an application that allows a user create and manage multiple shopping lists.

## Features

* The landing page includes a button to login/logout and a button to go to the lists dashboard (they both do the same thing but this is for better UX for both existing and new users)
* Login with Google account is required to access the lists dashboard
* Navigation bar in the dashboard is the same as on the homapge for consistency
* A greeting in the dashboard is displayed using users nickname so they know which account they are logged in with
* User can add a new list by writing its name in 'Add a new list field' and submit by clicking 'Add' button. The list name can have maximum 12 characters, next to the input field there is character counter that displays how many characters (out of max) remain to insert. The input is required and it will not be submitted empty. 
* A new created list appears in the drop down list of all lists and is automatically selected so the items can be added to it.
* If a user attempts to add a list using the same name as an existent list, the existing list is automatically selected and a message "You already have a list with this name." appears above below the drop down list. There is no limit how many lists can be added.
* 'Your lists' drop down includes all the lists of the user. Once a list is selected its items (if there are any) are displayed in the list area and it's name is displayed after 'Selected:' above the list area. 
* 'Delete this list button' deletes the selected list together with all the items. The application goes back to the state right after login - no list is selected. If the button is clicked in this state, nothing happens.
* If there is no list chosen, the message "Choose a list or create a new one to add items." is displayed in the list area to instruct the user how to start adding items. 
* 'Add an item' field allows to add new items to the selected list. Similarly to the 'Add new list', this field is required and has characters limit and remianing characters tracker. 
* If a user attempts to add an item when no list is selected, an alert will be triggered to inform that they need to choose a list o create a new one first. 
* If a list is selected and the input is not empty, the item is added to the list, after submitting by clicking 'add' button, and is displayed in the list area.
* Unlike with the list name, the items do not have to be unique, so a user can add the same item multiple times if she/he wishes to. There is no limit how many items can be added. 
* The 'Delete all items' button deletes all the items from the selected list. If there is no list selected or the list is empty, nothing happens when the button is clicked. 
* All the list items are displayed in the list area with edit and delete buttons next to them, if the items are so many that don't fit, the list area becomes scrollable.
* Each item can be edited by clicking a button with the edit symbol next to it. When the button is clicked, an input field becomes visible and editable, also the 'save' button appears. 
* The characters limit for the edit is the same as for adding. 
* When the 'save' button is clicked, the new value is saved and the item presentation comes back to the state from before the edit with the changed value (i.e. 'save' button disappears').
* Each item can be deleted by clicking the button with a symbol 'x' next to it.
* The application is responsive on multiple devices (e.g. desktop, mobile, tablet)

### Some possible features that could be added

* Possibility to mark items as bought/done (e.g. a checkbox; when checked the item name gets crossed out)
* Warning before deleting items or lists

### Known bugs

* When an item is edited, the whole text can be deleted and it can be saved blank. This is inconsistent with the fact that when adding item, the field is required so it is impossible to add empty item. As the edit input is readonly (this is removed with javascript when the edit button is pressed), required does not work with it, as it is not supported by HTML. I have tried to add required with javascript when readonly is removed, however readonly attribute is back when the change is submitted so the confilct remains. Unfortunately, I did not have more time to investigate how to do this correctly. 

## Technologies Used

* Python
* JavaScript
* [Google AppEngine](https://cloud.google.com/appengine)
* [Google Datastore NDB Client Library](https://cloud.google.com/appengine/docs/standard/python/ndb) 
* HTML
* CSS
* [Bootstrap](https://getbootstrap.com/)
* [Visual Studio Code](https://code.visualstudio.com/) - an IDE used to write the code
* [Git](https://git-scm.com/) - used for version control
* [Font Awesome](https://fontawesome.com/) - all the icons on the website 

## How to build and run the application

1. To start you need to create a new project (or get existing one) in [Google Cloud Console](https://console.cloud.google.com/)
2. Install (if you haven't already) [Google Cloud SDK](https://cloud.google.com/sdk/docs) that includes a local development server and the gcloud command-line for deploying and managing your apps.
3. Initialize gcloud tool

### How to run locally

1. Clone the ShopIt application:

```
git clone https://github.com/Alicja-Malinowska/Shopping_List.git

```
2. Go to Shopping_list folder

```
cd Shopping_list

```

3. To start local development web server, run the below command:

```
dev_appserver.py ./

```
4. You can now view the app in your browser [http://localhost:8080/](http://localhost:8080/)
5. Please note that while development server accepts any email address to login, when the app is deployed, only a valid gmail address will be accepted and password will be required. 
6. If you wish to stop the development center press `Control + C`

### Deployment

1. To deploy the application run the command:

```
gcloud app deploy app.yaml index.yaml

```
2. To view the deployed application run the command:

```
gcloud app browse

```
