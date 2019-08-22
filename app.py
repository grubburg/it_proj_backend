from flask import Flask
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
GCScert = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

cred = credentials.Certificate('./it-proj-backend-250602-58ddd0292162.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/dbtest')
def db_test():
	return 'This route worked.'

if __name__ == '__main__':
    app.run()
