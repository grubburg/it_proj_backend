from flask import Flask, request, g
import numpy as np
import tensorflow as tf
import os
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

from google.cloud import storage as gstorage

cred = credentials.Certificate(
    'it-proj-backend-firebase-adminsdk-pnizj-2ab146748a.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'it-proj-backend.appspot.com'
})


def create_app():
    app = Flask(__name__)

    with app.app_context():

        g.db = firestore.client()
        g.bucket = storage.bucket()
        g.client = gstorage.Client.from_service_account_json(
            'it-proj-backend-firebase-adminsdk-pnizj-2ab146748a.json')
        g.gstorage = gstorage
        from .family import family_routes
        from .item import item_routes
        from .user import user_routes
        from .detection import detection_routes

        app.register_blueprint(family_routes.family_bp)
        app.register_blueprint(item_routes.item_bp)
        app.register_blueprint(user_routes.user_bp)
        app.register_blueprint(detection_routes.detection_bp)

        return app
