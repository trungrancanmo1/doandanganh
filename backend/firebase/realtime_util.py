from pathlib import Path
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


options = {
    'databaseURL': 'https://ai-testings-d8cf2-default-rtdb.asia-southeast1.firebasedatabase.app/',
    # 'storageBucket': '', 
    # 'projectId': '', 
    # 'databaseAuthVariableOverride': '', 
    # 'serviceAccountId': '',
    # 'httpTimeout': '',
}


def connect_realtime():
    credential = credentials.Certificate(Path(os.getenv("CREDENTIALS_LOCATION", "VARIABLE NOT SET")))
    firebase_admin.initialize_app(credential, options)
    return db.reference(path='/', app=firebase_admin.initialize_app(credential, options, name='realtime'))


if __name__ == "__main__":
    new_data_1 = {
        "tem": 70,
        "humid": 3.50,
        "soil": 3.5
    }

    new_data_2 = {
        "tem": 77,
        "humid": 3.4,
        "soil": 1.12
    }

    new_data_3 = {
        "tem": 100,
        "humid": 3.45,
        "soil": 1.39
    }
    realtime_db = connect_realtime()
    realtime_db.child('sensors').child('sensor_1').update(new_data_1)
    realtime_db.child('sensors').child('sensor_2').update(new_data_2)
    realtime_db.child('sensors').child('sensor_3').set(new_data_3)