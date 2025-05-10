import firebase_admin
from firebase_admin import credentials, firestore, auth

cred = credentials.Certificate("../avi-cdtm-hack-team-1613-firebase-adminsdk-fbsvc-14ccd2ea46.json")
firebase_admin.initialize_app(cred)

db = firestore.client()