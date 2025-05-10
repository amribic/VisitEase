import firebase_admin
from firebase_admin import credentials, auth, firestore
import os
from pathlib import Path

def initialize_firebase():
    try:
        # Check if Firebase is already initialized
        firebase_admin.get_app()
    except ValueError:
        # Initialize Firebase if not already initialized
        # Get the absolute path to the credentials file
        cred_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'avi-cdtm-hack-team-1613-firebase-adminsdk-fbsvc-14ccd2ea46.json')
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

def get_firestore_db():
    initialize_firebase()
    return firestore.client()

def get_auth():
    initialize_firebase()
    return auth