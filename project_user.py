from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import asc
from database_setup import Base, Category, Item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

''' Import custom files '''

from user_functions import createUser, getUserID, getUserInfo, userIsLoggedIn, userIsOwner, showLogin
from base import session
from social_login import fbconnect, fbdisconnect, gconnect, gdisconnect, disconnect
from api import *

#Create flask application
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('google_client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Inventory App"
app.add_url_rule('/login', 'showLogin', showLogin)

''' Define Routes '''

#Authentication URLs
app.add_url_rule('/fbconnect', 'fbconnect', fbconnect, methods = ['POST', 'GET'])
app.add_url_rule('/fbdisconnect', 'fbdisconnect', fbdisconnect, methods = ['POST', 'GET'])
app.add_url_rule('/gconnect', 'gconnect', gconnect, methods = ['POST', 'GET'])
app.add_url_rule('/gdisconnect', 'gdisconnect', gdisconnect, methods = ['POST', 'GET'])
app.add_url_rule('/disconnect', 'disconnect', disconnect)

#Category URLs
app.add_url_rule('/', 'showCategories', showCategories)
app.add_url_rule('/categories/', 'showCategories', showCategories)
app.add_url_rule('/categories/new', 'newCategory', newCategory, methods = ['POST', 'GET'])
app.add_url_rule('/categories/<int:category_id>', 'showItems', showItems)
app.add_url_rule('/categories/<int:category_id>/items/', 'showItems', showItems)
app.add_url_rule('/categories/<int:category_id>/delete/', 'deleteCategory', deleteCategory, methods = ['POST', 'GET'])
app.add_url_rule('/categories/<int:category_id>/edit/', 'editCategory', editCategory, methods = ['POST', 'GET'])

#Category item URLs
app.add_url_rule('/categories/<int:category_id>/items/', 'showItems', showItems)
app.add_url_rule('/categories/<int:category_id>/items/new', 'newCategoryItem', newCategoryItem, methods = ['POST', 'GET'])
app.add_url_rule('/categories/<int:category_id>/items/<int:item_id>/', 'showItem', showItem)
app.add_url_rule('/categories/<int:category_id>/items/<int:item_id>/delete', 'deleteItem', deleteItem, methods = ['POST', 'GET'])
app.add_url_rule('/categories/<int:category_id>/items/<int:item_id>/edit', 'editItem', editItem, methods = ['POST', 'GET'])

#JSON endpoints
app.add_url_rule('/JSON/categories/', 'categoriesJSON', categoriesJSON)
app.add_url_rule('/JSON/categories/<int:category_id>/', 'categoryItemsJSON', categoryItemsJSON)
app.add_url_rule('/JSON/categories/<int:category_id>/items/<int:item_id>/', 'itemJSON', itemJSON)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)