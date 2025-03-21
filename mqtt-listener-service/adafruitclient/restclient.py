'''
- Rest API client of ada fruit IO
'''
from Adafruit_IO import Client, Feed
from config import IO_USERNAME, IO_KEY
from .logger import logger


rest_client = Client(username=IO_USERNAME, key=IO_KEY)


def add_feed(group_name : str, feed_name : str):
    feed = Feed(name=feed_name)
    response = rest_client.create_feed(feed=feed, group_key=group_name)
    logger.info(f'Feed { response } created')