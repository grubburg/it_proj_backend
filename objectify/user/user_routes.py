"""
User route blueprint for objectify app.
Created by Compu-global-hyper-mega-net for
COMP30022 IT Project Semester 2 2019.

Defines the following routes:


/user/signup/
    - Registers a user to the database

/user/info/
    - Returns information for a registered user

/user/info/families/
    - Returns a list of families of which the user is a member.

"""


#################### IMPORTS ###################

from flask import Blueprint, request, g
from flask import current_app as app
import firebase_admin
from firebase_admin import auth
from objectify.schemas.user import User
from objectify.schemas.family import Family
from objectify.schemas.item import Item

################################################

user_bp = Blueprint("user_bp", __name__)


db = g.db


################## USER ROUTES #################

"""
Create a new user in the database.
Valid fireauth token must be provided.
"""
@user_bp.route('/user/signup/', methods=['POST'])
def signUp():

    id_token = request.headers['Authorization'].split(' ').pop()
    data = request.get_json()

    # retrieve and decode the users token
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']

    # ad an empty list of items to the user object
    # data['items'] = []

    # remove the token from the user object
    user = User(data['name'], data['email'])
    dp_status = data['image']

    if dp_status == "true":
        user.image = "true"

    # add the user to the db, index by their UID
    db.collection(u'users').document(uid).set(user.to_dict())

    return str(data)


"""
Send a fireauth token and retrieve a given users information.
NOTE: This is not a session management function, it simply serves
to supply the app with user information.
"""
@user_bp.route('/user/info/')
def login():
    # capture the request data and retrieve uid from token
    # data = request.get_json()
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    # collect the user doc from the database
    user_data = db.collection(u'users').document(uid).get()

    return str(user_data.to_dict())


@user_bp.route("/user/info/families/")
def getAllFamilies():
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']

    user_ref = db.collection(u'users').document(uid)

    user = User.from_dict(user_ref.get().to_dict())

    family_token_list = list(user.families)

    family_dict = {}

    for token in family_token_list:
        family_ref = db.collection(u'families').document(token)

        family_dict[token] = family_ref.get().to_dict()

    return str(family_dict)


@user_bp.route("/user/info/families/other/")
def getAllOtherFamilies():
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']

    user_ref = db.collection(u'users').document(uid)

    user = User.from_dict(user_ref.get().to_dict())

    family_token_list = list(user.families)

    current_family = user.currentfamily

    family_token_list.remove(current_family)

    family_dict = {}

    for token in family_token_list:
        family_ref = db.collection(u'families').document(token)

        family_dict[token] = family_ref.get().to_dict()

    return str(family_dict)


@user_bp.route("/user/delete/")
def deleteUser():
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']

    user_ref = db.collection(u'users').document(uid)

    user_ref.delete()

    return "User deleted Successfuly"
