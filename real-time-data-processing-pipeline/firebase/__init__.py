'''
    - Giving the credentials
    - Creating a db to access the real time database
    - referenced from https://firebase.google.com/docs/firestore/quickstart#python
'''
from .firestore_util import connect_firestore

firestore_db = connect_firestore()