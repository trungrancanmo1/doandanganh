'''
    - Giving the credentials
    - Creating a db to access the real time database
    - referenced from https://firebase.google.com/docs/firestore/quickstart#python
'''
from .firestore_util import connect_firestore
import warnings

firestore_db = connect_firestore()

warnings.warn(
    "The 'my_package' package is deprecated and will be removed in future versions. "
    "Consider using 'new_package' instead.",
    DeprecationWarning,
    stacklevel=2
)