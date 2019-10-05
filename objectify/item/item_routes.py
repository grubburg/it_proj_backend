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

    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']

    user_ref = db.collection(u'users').document(uid)
    user = User.from_dict(user_ref.get().to_dict())
    current_family = user.currentfamily

    current_family_ref = db.collection(u'families').document(current_family)
    current_family = Family.from_dict(current_family_ref.get().to_dict())
    item_id_list = current_family.items

    item_dict = {}

    for item_id in item_id_list:
        item_ref = db.collection(u'items').document(item_id)
        item = Item.from_dict(item_ref.get().to_dict())
        print(type(item.visibility))
        if not item.visibility:
            item_dict[item_id] = item.to_dict()
        else:
            if uid in item.visibility:
                item_dict[item_id] = item.to_dict()

    return str(item_dict)


@item_bp.route('/item/add/', methods=['POST'])
def addItem():
    data = request.get_json()
    print(data)
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']

    user_ref = db.collection(u'users').document(uid)
    user = User.from_dict(user_ref.get().to_dict())
    current_family = user.currentfamily

    family_ref = db.collection(u'families').document(current_family)
    family = Family.from_dict(family_ref.get().to_dict())

    item = Item.from_dict(data)
    item_ref = db.collection(u'items').document()
    item_ref.set(item.to_dict())

    family.items.append(item_ref.id)

    family_ref.set(family.to_dict())

    # batch = db.batch()

    # batch.set(family_ref, family, merge=True)
    # #batch.set(item_ref, item)

    # batch.commit()

    return str(item.to_dict())


@item_bp.route("/item/add/ref/")
def getItemRef():
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']

    user_ref = db.collection(u'users').document(uid)
    user = User.from_dict(user_ref.get().to_dict())
    current_family = user.currentfamily

    family_ref = db.collection(u'families').document(current_family)
    print(family_ref.get().to_dict())
    family = Family.from_dict(family_ref.get().to_dict())
    print(family)
    num_items = len(family.items)
    family_token = family.token

    resp = {family_token: num_items}

    return str(resp)