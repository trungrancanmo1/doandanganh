'''
    @zun
    - the package of MQTT handlers
    - run in a separated thread, apart from API handler
    of Django
'''
from Adafruit_IO import MQTTClient
import os
from .handlers import FEEDS
from .handlers import FEED_HANDLERS
from dotenv import load_dotenv
from .logger import logger
from firebase import firestore_db
from google.cloud.firestore_v1 import FieldFilter


load_dotenv(dotenv_path='./.env')


# getting API key from environment variable
IO_USERNAME = os.getenv('IO_USERNAME', 'DEFAULT')
IO_KEY = os.getenv('IO_KEY', 'DEFAULT')
client = MQTTClient(IO_USERNAME, IO_KEY)


def connected(client : MQTTClient):
    '''
    - Query the database and subscribe for all activated sensors
    '''
    # subcribe for these feeds
    # for feed_id in FEEDS.values():
    #     client.subscribe(feed_id=feed_id)
    #     logger.info(f'Subscribe to {feed_id}')
    topics = firestore_db.collection('sensors').where(filter=FieldFilter('status', '==', True)).select(['topic']).get()

    for topic in topics:
        topic = topic.to_dict().get('topic')
        client.subscribe(topic)
        logger.info(f'Subscribe to { topic }')


def message(client : MQTTClient, feed_id, new_value):
    # call the appropriate handler
    # if data is generated continously
    # it is native blocking
    if feed_id in FEEDS.values():
        FEED_HANDLERS[feed_id](new_value)


def add_new_sensor_api_creating_new_topic_in_ada_fruit_subscribe_collecting_data():
    pass


def mqtt_listener():
    '''
        start the mqtt service
    '''
    # set up MQTT client
    client.on_connect = connected
    client.on_message = message

    # connect to MQTT broker
    client.connect()

    # for testings
    client.loop_blocking()