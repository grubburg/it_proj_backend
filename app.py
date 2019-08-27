from flask import Flask, request

import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
# GCScert = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

cred = credentials.Certificate('./it-proj-backend-250602-58ddd0292162.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
app = Flask(__name__)


@app.route('/')
def hello_world():
	return "compu-global-hyper-mega-net was here!"


@app.route('/items/add', methods = ['POST'])
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



if __name__ == '__main__':
    app.run(debug=True)
