import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from config.config import SERVICE_ACCOUNT_KEY


# Use a service account.
credential = credentials.Certificate(SERVICE_ACCOUNT_KEY)
app = firebase_admin.initialize_app(credential=credential)
db = firestore.client()