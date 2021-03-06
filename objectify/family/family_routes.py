"""
Family route blueprint for objectify app.
Created by Compu-global-hyper-mega-net for
COMP30022 IT Project Semester 2 2019.

Defines the following routes:

"""


#################### IMPORTS ###################
from flask import Blueprint, request, g
from flask import current_app as app
from flask_api import status
from objectify.schemas.user import User
from objectify.schemas.family import Family
from objectify.schemas.item import Item

import secrets
import firebase_admin
from firebase_admin import auth
################################################


#################### GLOBALS ###################

# create the family blueprint
family_bp = Blueprint("family_bp", __name__)

db = g.db  # reference the firestore client
################################################


#################### GLOBALS ###################
def getUserFromRequest(request):

    # retrieve use token from database
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']

    # retrieve current user and current family
    user_ref = db.collection(u'users').document(uid)
    user = User.from_dict(user_ref.get().to_dict())

    return uid, user

################################################


################# FAMILY ROUTES ################

@family_bp.route('/family/create/', methods=['POST'])
def createFamily():
    # capture request data and retrieve uid from token
    data = request.get_json()

    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    if not uid:
        return status.HTTP_401_UNAUTHORIZED

    # retrieve the users current list of families
    user_data = db.collection(u'users').document(uid).get()
    user_data = user_data.to_dict()
    current_families = user_data['families']

    # create family object
    name = data['name']
    family = Family(name)

    family.members = [uid]
    family_token = secrets.token_urlsafe(8)
    family.token = family_token
    current_families.append(family_token)

   # batched write to database
    batch = db.batch()
    user_ref = db.collection(u'users').document(uid)
    batch.update(
        user_ref, {u'currentfamily': family_token, u'families': current_families})

    family_ref = db.collection(u'families').document(family_token)

    batch.set(family_ref, family.to_dict())

    batch.commit()

    return str(family.to_dict())


"""
Retrieve the join token of a users current family. If the user
is not currently part of a family, an error is returned.
"""
@family_bp.route('/family/token/')
def getFamilyToken():

    # Capture request data and extract user id from token.
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    if not uid:
        return status.HTTP_401_UNAUTHORIZED
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


@family_bp.route('/family/join/', methods=['POST'])
def joinFamily():

    # capture request data and extract uid from token
    data = request.get_json()
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    if not uid:
        return status.HTTP_401_UNAUTHORIZED
    # extract family identifier from request
    family_token = data['family_token']

    # find family in the database. If the family does not exist,
    # return a not_found status code.
    family_ref = db.collection(u'families').document(family_token)
    doc = family_ref.get()

    if not doc.exists:
        return "Family not found!", status.HTTP_404_NOT_FOUND

    family = Family.from_dict(doc.to_dict())
    user_ref = db.collection(u'users').document(uid)
    # add the family id to the users list of families.
    user = User.from_dict(user_ref.get().to_dict())
    user_families = user.families
    user_families.append(family_token)

    # add the user to the family's list of members.
    members = family.members
    members.append(uid)

    # commit changes to the database in a batch
    batch = db.batch()
    batch.update(
        user_ref, {'currentfamily': family_token, 'families': user_families})
    batch.update(family_ref, {'members': members})
    batch.commit()

    return str(family.to_dict())


"""
returns:
    - family name
    - invite code
    - list of members names
"""


@family_bp.route("/family/info/", methods=['POST'])
def getFamilyInfo():

    data = request.get_json()
    family_token = data['family_token']
    uid, user = getUserFromRequest(request)

    if not uid:
        return status.HTTP_401_UNAUTHORIZED

    family_ref = db.collection(u'families').document(family_token)
    family = Family.from_dict(family_ref.get().to_dict())

    resp = {}
    resp['name'] = family.name
    resp['family_token'] = family_token

    names = []
    for member in family.members:
        u_ref = db.collection('users').document(member)
        name = u_ref.get().to_dict()['name']

        names.append(name)

    resp['members'] = names

    return str(resp)


@family_bp.route("/family/curr/members/")
def getFamilyMembers():

    # extract uid from auth token
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']

    if not uid:
        return status.HTTP_401_UNAUTHORIZED

    # retrieve user from database
    user_ref = db.collection(u'users').document(uid)
    user = User.from_dict(user_ref.get().to_dict())

    # retrieve current family from database
    family_token = user.currentfamily
    family_ref = db.collection(u'families').document(family_token)
    family = Family.from_dict(family_ref.get().to_dict())

    # construct a list of family members and return it
    member_ids = family.members

    family_member_dict = {}

    # TODO filter out family membership field from other family members

    for member_id in member_ids:
        member_ref = db.collection(u'users').document(member_id)
        member = User.from_dict(member_ref.get().to_dict())
        family_member_dict[member_id] = member.to_dict()

    return str(family_member_dict)


@family_bp.route("/family/switch/", methods=['POST'])
def switchFamily():

    data = request.get_json()

    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    if not uid:
        return status.HTTP_401_UNAUTHORIZED

    # retrieve user from database
    user_ref = db.collection(u'users').document(uid)

    new_family_token = data['family_token']

    user_ref.set({"currentfamily": new_family_token}, merge=True)
    return str(data)


@family_bp.route("/family/leave/", methods=['POST'])
def leaveFamily():

    data = request.get_json()
    id_token = request.headers['Authorization'].split(' ').pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']

    user_ref = db.collection(u'users').document(uid)

    user = User.from_dict(user_ref.get().to_dict())

    family_token = data['family_token']

    family_ref = db.collection(u'families').document(family_token)
    family = Family.from_dict(family_ref.get().to_dict())
    family.members.remove(uid)

    user.families.remove(family_token)

    if user.currentfamily == family_token:
        user.currentfamily = user.families[0]

    batch = db.batch()

    batch.set(family_ref, family.to_dict())
    batch.set(user_ref, user.to_dict())

    batch.commit()

    if len(family.members == 0):
        for item in family.items:
            item_ref = db.collection(u'items').document(item)
            item_ref.delete()
        family_ref.delete()

    return str(family.to_dict())
