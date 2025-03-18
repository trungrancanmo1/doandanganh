'''
    - Giving the credentials
    - Creating a db to access the FireStore
'''
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
import os


def connect():
    credentials_path = Path(os.getenv("CREDENTIALS_LOCATION", "VARIABLE NOT SET"))
    credential = credentials.Certificate(credentials_path)
    firebase_admin.initialize_app(credential)
    return firestore.client()


if __name__ == '__main__':
    connect()