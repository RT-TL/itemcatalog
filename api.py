from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import asc
from database_setup import Base, Category, Item, User
from base import session
from user_functions import *

'''JSON API'''

#Show JSON list of category items
def categoryItemsJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])

#Show JSON of item details
def itemJSON(category_id, item_id):
    items = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=items.serialize)

#Show JSON category list
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


''' USER ENDPOINTS '''

# Show all categories
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('categories.html', categories=categories)


# Create a new category
def newCategory():
    if not userIsLoggedIn():
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        newCategory.user_id = login_session['user_id']
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')


# Edit a category
def editCategory(category_id):
    editedCategory = session.query(
        Category).filter_by(id=category_id).one()

    if not userIsOwner(editedCategory.user_id):
        return redirect(url_for('showLogin'))

    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Category Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('showItems', category_id = category_id))
    else:
        return render_template('editCategory.html', category=editedCategory)


# Delete a category
def deleteCategory(category_id):
    categoryToDelete = session.query(
        Category).filter_by(id=category_id).one()

    if not userIsOwner(categoryToDelete.user_id):
        return redirect(url_for('showLogin'))

    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        return render_template('deleteCategory.html', category=categoryToDelete)


# Show a category items
#@app.route('/categories/<int:category_id>/')
#@app.route('/categories/<int:category_id>/items/')
def showItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()

    # Get creator data
    creator = getUserInfo(category.user_id)

    template = 'publicmenu.html'

    if userIsOwner(category.user_id):
        template = 'items.html'

    return render_template(template, items=items, category=category, creator=creator)


# Create a new item
#@app.route('/categories/<int:category_id>/items/new/', methods=['GET', 'POST'])
def newCategoryItem(category_id):
    if not userIsLoggedIn():
        return redirect(url_for('showLogin'))

    #Find requested category
    category = session.query(Category).filter_by(id=category_id).one()

    #Handle form submit
    if request.method == 'POST':
        newItem = Item(name=request.form['name'], description=request.form[
            'description'], price=request.form['price'], category_id=category_id)

        #Assign creator id
        newItem.user_id = login_session['user_id']

        #Store new item
        session.add(newItem)
        session.commit()

        flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id)


# Edit an item
def editItem(category_id, item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()

    if not userIsOwner(editedItem.user_id):
        return redirect(url_for('showLogin'))

    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        flash('Item Successfully Edited')
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('edititem.html', category_id=category_id, item_id=item_id, item=editedItem)

#Display Item
def showItem(category_id, item_id):
    #Fetch display data
    displayItem = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()

    return render_template('itemdetails.html', category_id=category_id, item_id=item_id, item=displayItem)



# Delete a menu item
def deleteItem(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    itemToDelete = session.query(Item).filter_by(id=item_id).one()

    if not userIsOwner(itemToDelete.user_id):
        return redirect(url_for('showLogin'))

    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deleteItem.html', item=itemToDelete)