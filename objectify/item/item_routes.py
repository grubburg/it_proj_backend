"""
Item route blueprint for objectify app.
Created by Compu-global-hyper-mega-net for
COMP30022 IT Project Semester 2 2019.

Defines the following routes:

/item/list/
    - list all the items visible to the current user

/item/add/
    - add an item to the database


/item/add/ref/
    - return the number of items currently in the database 
      for a given family. 
      Used in order to create references to stored images.
      

"""



#################### IMPORTS ###################
from flask import Blueprint, request, g
from flask import current_app as app

from objectify.schemas.user import User
from objectify.schemas.family import Family
from objectify.schemas.item import Item

import firebase_admin
from firebase_admin import auth
################################################



#################### GLOBALS ###################

#create the item blueprint
item_bp = Blueprint("item_bp", __name__)

# reference the firestore client
db = g.db
################################################




################## ITEM ROUTES #################

@item_bp.route('/item/list/')
def getAllItems():

    # retrieve use token from database
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']

    # retrieve current user and current family
    user_ref = db.collection(u'users').document(uid)
    user = User.from_dict(user_ref.get().to_dict())
    current_family = user.currentfamily
    current_family_ref = db.collection(u'families').document(current_family)
    current_family = Family.from_dict(current_family_ref.get().to_dict())
    
    # retrieve list of items in current family
    item_id_list = current_family.items


    # create and return dictionary
    item_dict = {}

    for item_id in item_id_list:
        item_ref = db.collection(u'items').document(item_id)
        item = Item.from_dict(item_ref.get().to_dict())
        
        # if the visibility array is empty, this implies 
        # global visibility
        if "global" in item.visibility:
            item_dict[item_id] = item.to_dict()
        # if not empty, we check if the user is explicity
        # allowed to view the item.
        else:
            if uid in item.visibility:
                item_dict[item_id] = item.to_dict()

    return str(item_dict)


@item_bp.route('/item/add/', methods=['POST'])
def addItem():

    # retrieve request data and user ID from request
    data = request.get_json()
    
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']

    # retrieve user and current family from database
    user_ref = db.collection(u'users').document(uid)
    user = User.from_dict(user_ref.get().to_dict())
    current_family = user.currentfamily
    family_ref = db.collection(u'families').document(current_family)
    family = Family.from_dict(family_ref.get().to_dict())

    # create the item object from the request data and 
    # create its database reference
    item = Item.from_dict(data)
    item_ref = db.collection(u'items').document()
    
    batch = db.batch()

    batch.set(item_ref, item.to_dict())
    
    #item_ref.set(item.to_dict())

    family.items.append(item_ref.id)

    batch.set(family_ref, family.to_dict())
    #family_ref.set(family.to_dict())

    batch.commit()

    return str(item.to_dict())


@item_bp.route("/item/add/ref/")
def getItemRef():
    
    
    # retrieve user token and id from request
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']

    # retrieve user from dp
    user_ref = db.collection(u'users').document(uid)
    user = User.from_dict(user_ref.get().to_dict())
    current_family = user.currentfamily

    family_ref = db.collection(u'families').document(current_family)
    
    # construct the family object
    family = Family.from_dict(family_ref.get().to_dict())
    
    num_items = len(family.items)
    family_token = family.token

    resp = {family_token: num_items}

    return str(resp)