from config import *


import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.enums import MQTTProtocolVersion
import json
import serial
import time

ser = serial.Serial(
    port='COM22',  # Replace with your serial port
    baudrate=115200,  # Replace with your desired baud rate
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1  # Optional: Set a timeout for reading
)

def send_to_device(data):
    try:
        # Send the data
        ser.write(data.encode('utf-8'))
        print(f"Sent: {data}")

    except serial.SerialException as e:
        print(f"Error opening or communicating with serial port: {e}")
        
        
# =================================================
# SUBSCRIBING FOR ONLY USER'S DEVICES
# =================================================
COMMAND_TOPIC = make_topic('+', 'command', '+')


def on_connect(mqttc, obj, flags, rc, properties):
    mqttc.subscribe(topic=COMMAND_TOPIC)


# =================================================
# ON_MESSAGE CALL-BACK
# =================================================
def on_message(mqttc, obj, msg):
    # decode the payload
    data = json.loads(msg.payload.decode('utf-8'))
    print(f"Received data: {data}")

    # control device
    type = data['type'][:3]
    value = int(data['value'])
    send_data = f"{type}_{value}"
    send_to_device(send_data)


def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
    # logger.info("Subscribed: " + str(mid) + " " + str(reason_code_list))
    print("Subscribed: " + str(mid) + " " + str(reason_code_list))


def on_log(mqttc, obj, level, string):
    print(string)


mqtt_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTProtocolVersion.MQTTv5)
mqtt_client.username_pw_set(username=EMQX_USER_NAME, password=EMQX_PASSWORD)

mqtt_client.connect(host=EMQX_URL, port=1883)


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_subscribe = on_subscribe

mqtt_client.loop_forever()