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
load_dotenv(dotenv_path='./.env')


def connected(client : MQTTClient):
    # subcribe for these feeds
    for feed_id in FEEDS.values():
        client.subscribe(feed_id=feed_id)
        logger.info(f'Subscribe to {feed_id}')


def message(client, feed_id, new_value):
    # call the appropriate handler
    # if data is generated continously
    # it is native blocking
    if feed_id in FEEDS.values():
        FEED_HANDLERS[feed_id](new_value)


def mqtt_subscriber_start():
    '''
        start the mqtt service
    '''
    # getting API key from environment variable
    IO_USERNAME = os.getenv('IO_USERNAME', 'DEFAULT')
    IO_KEY = os.getenv('IO_KEY', 'DEFAULT')

    # set up MQTT client
    client = MQTTClient(IO_USERNAME, IO_KEY)
    client.on_connect = connected
    client.on_message = message

    # connect to MQTT broker
    client.connect()

    # for testings
    client.loop_blocking()

    # for production, running on
    # another threads
    # client.loop_background()