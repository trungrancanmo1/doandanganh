'''
    @zun
    - define the handler when
    receiving message from MQTT broker
'''
from .logger import logger
# features : feed_id
FEEDS = {
    "temperature":  "trungdung1711.temperature",
    "humidity":     "trungdung1711.humidity",
    "light":        "trungdung1711.light"
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