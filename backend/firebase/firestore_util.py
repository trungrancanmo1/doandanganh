'''
    - Giving the credentials
    - Creating a db to access the FireStore
'''
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
import os


def connect_firestore():
    credential = credentials.Certificate(Path(os.getenv("CREDENTIALS_LOCATION", "VARIABLE NOT SET")))
    return firestore.client(app=firebase_admin.initialize_app(credential, name='firestore'))


if __name__ == '__main__':
    connect_firestore()