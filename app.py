
from flask import Flask, request
from schemas.user import User
from schemas.item import Item
from schemas.family import Family
import os
import secrets

import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import firestore


# Load firebase credentials and authenticate firebase admin
# ------------------------------------------------------------
cred = credentials.Certificate(
    './it-proj-backend-firebase-adminsdk-pnizj-2ab146748a.json')
firebase_admin.initialize_app(cred)
# -------------------------------------------------------------

# Create app and database objects
# -------------------------------------------------------------
db = firestore.client()
app = Flask(__name__)
# -------------------------------------------------------------


################ ROUTES ###############
"""
Base route. TODO: replace with something meaniful 
"""
@app.route('/')
def hello_world():
    return "compu-global-hyper-mega-net was here!"

@app.route('/test/', methods=['POST'])
def testroute():
    data = request.get_json()

    first = data['first']
    item = first['1']
    return str(item)
"""
Add an item to the database. 
TODO: add logic to add item to a users list of items.
"""
@app.route('/items/add', methods=['POST'])
def addItem():
    data = request.get_json()
    db.collection(u'items').add(data)
    return str(data)


"""
List all items in the database
TODO: List only items for a given user. 
"""
"""
@app.route('/items/')
def getAllItems():
    items = db.collection(u'items').stream()
    itemstr = ''
    for item in items:

        itemstr += str(item.to_dict()) + '\n'
    return itemstr
"""

@app.route('/useritems/')
def getAllItems():
    
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    user_data = db.collection(u'users').document(uid).get()
    user_dict = user_data.to_dict()

    items = user_data['items']
    
    return str(items)



"""
Create a new user in the database.
Valid fireauth token must be provided. 
"""
@app.route('/signup/', methods=['POST'])
def signUp():
    
    id_token = request.headers['Authorization'].split(' ').pop()
    data = request.get_json()

    # retrieve and decode the users token
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    
    # ad an empty list of items to the user object
    data['items'] = []
    
    # remove the token from the user object
    user = User(data['name'], data['email']) 
    # add the user to the db, index by their UID
    db.collection(u'users').document(uid).set(user.to_dict())

    return str(data)

"""
Send a fireauth token and retrieve a given users information.
NOTE: This is not a session management function, it simply serves
to supply the app with user information. 
"""
@app.route('/login/', methods=['POST'])
def login():
    # capture the request data and retrieve uid from token
    data = request.get_json() 
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    # collect the user doc from the database
    user_data = db.collection(u'users').document(uid).get()

    return str(user_data.to_dict())

@app.route('/createfamily/', methods=['POST'])
def createFamily():
    #capture request data and retrieve uid from token
    data = request.get_json()
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    

    name = data['name']
    family = Family(name)
    family.members.append(uid)
    family_token = secrets.token_urlsafe(8)
    family.token = family_token
    
    db.collection(u'families').document(family_token).set(family.to_dict())

    return str(family.to_dict())







if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
