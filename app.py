from flask import Flask, request
from schemas import user
import os

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
@app.route('/items/')
def getAllItems():
    items = db.collection(u'items').stream()
    itemstr = ''
    for item in items:

        itemstr += str(item.to_dict()) + '\n'
    return itemstr


"""
Create a new user in the database.
Valid fireauth token must be provided. 
"""
@app.route('/signup/', methods=['POST'])
def signUp():
    data = request.get_json()

    # retrieve and decode the users token
    id_token = data['token']
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    
    # ad an empty list of items to the user object
    data['items'] = []
    
    # remove the token from the user object
    del data['token']
    user = User(data) 
    # add the user to the db, index by their UID
    db.collection(u'users').document(uid).set(user.to_dict())

    return str(data)


# @app.route('/login/')
# def login():


if __name__ == '__main__':
    app.run(host='0.0.0.0')
