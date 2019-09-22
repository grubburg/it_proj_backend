from flask import Flask, request

import os

import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
# GCScert = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

cred = credentials.Certificate(
    './it-proj-backend-firebase-adminsdk-pnizj-2ab146748a.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "compu-global-hyper-mega-net was here!"


@app.route('/items/add', methods=['POST'])
def addItem():
    data = request.get_json()
    db.collection(u'items').add(data)
    return str(data)


@app.route('/items/')
def getAllItems():
    items = db.collection(u'items').stream()
    itemstr = ''
    for item in items:

        itemstr += str(item.to_dict()) + '\n'
    return itemstr


@app.route('/signup/', methods=['POST'])
def signUp():
    data = request.get_json()

    username = data['username']
    email = data['email']
    token = data['token']

    db.collection(u'users').document(token).set(data)

    return data


# @app.route('/login/')
# def login():


if __name__ == '__main__':
    app.run(host='0.0.0.0')
