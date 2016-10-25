from database_setup import Base, Category, Item, User
from flask import session as login_session
from flask import render_template
from base import session
import random, string

#Create new user account
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
        'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

#Get user info by ID
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

#Get user id by email
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

#Check if user is currently logged in
def userIsLoggedIn():
    if 'provider' in login_session:
        return True
    return False

#Check if current user has ownership rights
def userIsOwner(owner_id):
    if userIsLoggedIn():
        if login_session['user_id'] == owner_id:
            return True

    return False

def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)