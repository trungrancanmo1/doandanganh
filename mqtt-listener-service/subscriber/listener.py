'''
    @zun
    - the package of MQTT handlers
    - run in a separated thread, apart from API handler
    of Django
'''
from Adafruit_IO import MQTTClient
import os
from dotenv import load_dotenv
from .logger import logger
from firebase import firestore_db
from google.cloud.firestore_v1 import FieldFilter
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor
from .workers import worker
from .workers import data_queue


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
    topics = firestore_db\
    .collection('sensors')\
    .where(filter=FieldFilter('status', '==', True))\
    .select(['topic'])\
    .get()

    for topic in topics:
        topic = topic.to_dict().get('topic')
        client.subscribe(topic)
        logger.info(f'Subscribe to { topic }')


def message_v1(client : MQTTClient, feed_id : str, new_value):
    logger.warning('This function can be a bottle-neck and deprecated')
    # persist the data into the database
    # feed_id is now the sensors document id
    '''
    - Add a record in the sensor document
    '''
    if 'temperature' in feed_id:
        unit = 'C'
    elif 'humidity' in feed_id:
        unit = '%'
    elif 'light' in feed_id:
        unit = 'lx'

    record = {
        'data' : new_value,
        'timestamp' : datetime.now(),
        'unit' : unit
    }

    firestore_db\
    .collection('sensors', feed_id, 'records')\
    .add(record, str(record['timestamp']))
    logger.info(f'Persist data from {feed_id}')


def message_v2(client : MQTTClient, feed_id : str, new_value):
    '''
    - callback function when new data is collected
    - simply add records to the queue and let workers handle the record
    '''
    if 'temperature' in feed_id:
        unit = 'C'
    elif 'humidity' in feed_id:
        unit = '%'
    elif 'light' in feed_id:
        unit = 'lx'
    else:
        unit = 'unknown'

    # create a record
    record = {
        'feed_id': feed_id,
        'data': new_value,
        'timestamp': datetime.now(),
        'unit': unit
    }

    # store it to the queue
    data_queue.put(record)
    logger.info(f'Queued data from {feed_id}')


def mqtt_listener_workers_manager(num = 5):
    '''
    - A parent threads that create a pool of thread workers
    '''
    with ThreadPoolExecutor(max_workers=num) as executor:
        for _ in range(num):
            executor.submit(worker)


def mqtt_listener():
    '''
        - Start the mqtt service in one dedicated thread
        - That thread is blocking-behiviour in nature because of loop_blocking() of callbacks
    '''
    # set up MQTT client
    client.on_connect = connected
    client.on_message = message_v2

    # connect to MQTT broker
    client.connect()

    logger.info('Workers manager started, workers ready to work!')
    threading.Thread(target=mqtt_listener_workers_manager, name='workers_manager', args=(5, ), daemon=True).start()

    # for testings
    client.loop_blocking()