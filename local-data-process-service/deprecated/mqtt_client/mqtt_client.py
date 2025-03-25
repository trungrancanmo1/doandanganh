import paho.mqtt.client as mqtt
import dotenv
import os
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.enums import MQTTProtocolVersion
import json


dotenv.load_dotenv('./.env', verbose=True)
CEDALO_ACCESS_TOKEN=os.getenv('CEDALO_ACCESS_TOKEN')
CEDALO_MQTT_BROKER_URL=os.getenv('CEDALO_MQTT_BROKER_URL')

EMQX_USER_NAME=os.getenv('EMQX_USER_NAME')
EMQX_PASSWORD=os.getenv('EMQX_PASSWORD')
EMQX_URL=os.getenv('EMQX_URL')

# MQTT Broker details
PORT = 1883  # Use 8883 if connecting with TLS
TOPIC = "hcmut-smart-farm/+/+/+/+/data"


def on_connect(mqttc : mqtt.Client, obj, flags, reason_code, properties):
    print("reason_code: " + str(reason_code))
    mqttc.subscribe(topic=TOPIC)


def on_message(mqttc, obj, msg):
    # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    payload = json.loads(msg.payload.decode('utf-8'))
    print(payload['device_id'])


def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
    print("Subscribed: " + str(mid) + " " + str(reason_code_list))


def on_log(mqttc, obj, level, string):
    print(string)

# Create MQTT client
client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTProtocolVersion.MQTTv5)
client.username_pw_set(username=EMQX_USER_NAME, password=EMQX_PASSWORD)


# Assign callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(host=EMQX_URL, port=PORT, keepalive=60, clean_start=True)


# Keep the client running
client.loop_forever()