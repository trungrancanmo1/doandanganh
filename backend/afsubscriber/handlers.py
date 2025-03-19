'''
    @zun
    - define the handler when
    receiving message from MQTT broker
'''
# features : feed_id
FEEDS = {
    "temperature":  "smart-farm.temperature",
    "humidity":     "smart-farm.humidity",
    "light":        "smart-farm.light"
}


def handle_temperature(data):
    print('Handle temperature')
    # import time
    # time.sleep(15)


def handle_humidity(data):
    print('Handle humidity')


def handle_light(data):
    print('Handle light')


# feed_id : handlers
FEED_HANDLERS = {
    FEEDS["temperature"]: handle_temperature,
    FEEDS["humidity"]: handle_humidity,
    FEEDS["light"]: handle_light
}