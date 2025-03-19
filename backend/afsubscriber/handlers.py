'''
    @zun
    - define the handler when
    receiving message from MQTT broker
'''
from .logger import logger
# features : feed_id
FEEDS = {
    "temperature":  "smart-farm.temperature",
    "humidity":     "smart-farm.humidity",
    "light":        "smart-farm.light"
}


def handle_temperature(data):
    logger.info('Handle temperature data')


def handle_humidity(data):
    logger.info('Handle humidity data')


def handle_light(data):
    logger.info('Handle light data')


# feed_id : handlers
FEED_HANDLERS = {
    FEEDS["temperature"]: handle_temperature,
    FEEDS["humidity"]: handle_humidity,
    FEEDS["light"]: handle_light
}