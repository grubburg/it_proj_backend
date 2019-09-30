
from flask import Flask, request
from flask_api import status
from schemas.user import User
from schemas.item import Item
from schemas.family import Family
import os
import secrets
import google.cloud.exceptions


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

@app.route('/family/create/', methods=['POST'])
def createFamily():
    #capture request data and retrieve uid from token
    data = request.get_json()
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
   
    #retrieve the users current list of families 
    user_data = db.collection(u'users').document(uid).get()
    user_data = user_data.to_dict()
    current_families = user_data['families']
     
    #create family object
    name = data['name']
    family = Family(name)
    family.members.append(uid)
    family_token = secrets.token_urlsafe(8)
    family.token = family_token
    current_families.append(family_token)
   
   #batched write to database
    batch = db.batch()
    user_ref = db.collection(u'users').document(uid)
    batch.update(user_ref, {u'currentfamily':family_token,u'families': current_families})

    family_ref = db.collection(u'families').document(family_token)
    
    batch.set(family_ref, family)

    batch.commit()

    return str(family.to_dict())
"""
Retrieve the join token of a users current family. If the user
is not currently part of a family, an error is returned.
"""
@app.route('/family/token/')
def getFamilyToken():
    
    # Capture request data and extract user id from token.
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    doc_ref = db.collection(u'users').document(uid)
    # build the user object
    doc = doc_ref.get()
    user = User.from_dict(doc.to_dict())
    
    # if the token exists, return it. Otherwise return a 404
    token = user.currentfamily
    if token:
        return str(token)
    else:
        return "Error: user is not part of a family.", status.HTTP_404_NOT_FOUND


    
"""
Route to join a user to a family. The user provides a family
joining token, and in turn the family is added to the user's
list of families. 
"""

@app.route('/family/join', methods=['POST'])
def joinFamily():
    
    #capture request data and extract uid from token
    data = request.get_json()
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    #extract family identifier from request
    family_token = data['family_token']
    
    # find family in the database. If the family does not exist, 
    # return a not_found status code.
    family_ref = db.collection(u'families').document(family_token)
    doc = family_ref.get()
    
    if not doc.exists:
        return "Family not found!", status.HTTP_404_NOT_FOUND

   
    family = Family.from_dict(doc.to_dict())
    user_ref = db.collection(u'users').document(uid)
    #add the family id to the users list of families.   
    user = User.from_dict(user_ref.get().to_dict())
    user_families = user.families
    user_families.append(family_token)
    
    #add the user to the family's list of members.
    members = family.members
    members.append(uid)
    
    # commit changes to the database in a batch
    batch = db.batch()
    batch.update(user_ref, {'currentfamily': family_token, 'families': user_families})
    batch.update(family_ref, {'members': members})
    batch.commit()

    return "Family joined successfully."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
