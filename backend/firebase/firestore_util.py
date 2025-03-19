'''
    - Giving the credentials
    - Creating a db to access the FireStore
'''
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env')


def connect_firestore():
    credential = credentials.Certificate(Path(os.getenv("CREDENTIALS_LOCATION", "DEFAULT")))
    return firestore.client(app=firebase_admin.initialize_app(credential, name='firestore'))


if __name__ == '__main__':
    connect_firestore()