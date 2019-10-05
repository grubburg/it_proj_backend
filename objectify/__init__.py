from flask import Flask, request, g
# from flask_api import status
# import os
# import secrets
# import google.cloud.exceptions
# import ast

import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import firestore


# Load firebase credentials and authenticate firebase admin
# ------------------------------------------------------------
cred = credentials.Certificate(
    './it-proj-backend-firebase-adminsdk-pnizj-fc9aa8b559.json')
firebase_admin.initialize_app(cred)
# -------------------------------------------------------------

# Create app and database objects
# -------------------------------------------------------------



def create_app():
    app = Flask(__name__)

    with app.app_context():
        
        g.db = firestore.client()

        from .family import family_routes
        from .item import item_routes
        from .user import user_routes

        app.register_blueprint(family_routes.family_bp)
        app.register_blueprint(item_routes.item_bp)
        app.register_blueprint(user_routes.user_bp)




        return app