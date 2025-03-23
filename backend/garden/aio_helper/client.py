from Adafruit_IO import Client, MQTTClient

def get_aio_client(username: str, key: str, MQTT=False):
    return MQTTClient(username, key) if MQTT else Client(username, key)