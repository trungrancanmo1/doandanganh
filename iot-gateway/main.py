import serial
import time
import json
from datetime import datetime
from iot_gateway_to_mqtt_broker import send_to_broker

from config import *
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.enums import MQTTProtocolVersion


# Device setup
PORT = 'COM22'
BAUDRATE = 115200
TIMEOUT = 1

ser = serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT)
print(f"Serial port {PORT} opened successfully.")

        
# MQTT setup
  
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
    type = data['type']
    if type == 'light':
        type = 'ill'
    elif type == 'fan':
        type = 'ven'
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


# Helper function
def send_to_device(data):
    try:
        # Send the data
        ser.write(data.encode('utf-8'))
        print(f"Sent: {data}")

    except serial.SerialException as e:
        print(f"Error opening or communicating with serial port: {e}")
        
def send_to_broker(payload : bytes, topic : str):
    '''
    - call this function when you collect the full dictionary
    - data = {
        # fixed data
        ###########################################
        "user_id": "VVRsnPoAEqSbUa9QLwXLgj2D9Zx2",
        "env_id": "my_simple_garden",
        "sensor_id": "sensor_101",
        ###########################################
        "timestamp": "2024-03-25T12:05:00Z",
        "type": "temperature",
        "value": 40.0, ############## NOTE: always float
    }
    '''
    mqtt_client.publish(topic=topic, payload=payload, qos=2)
    print(f"Published data to topic '{topic}' successfully.")


def receive_serial_data():
    try:
        if ser.in_waiting > 0:
            received_bytes = ser.readline().strip()
            try:
                received_string = received_bytes.decode('utf-8')
                return received_string
            except UnicodeDecodeError:
                print(f"Error decoding received bytes: {received_bytes}")
                return None
        else:
            return None

    except serial.SerialException as e:
        print(f"Error opening serial port {PORT}: {e}")
        return None
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print(f"Serial port {PORT} closed.")
            
def parse_data_to_dict(data):
    data_dict = {}
    pairs = data.split(', ')

    for pair in pairs:
        key_value = pair.split(': ')
        if len(key_value) == 2:
            key = key_value[0].strip()
            value_str = key_value[1].strip()
            try:
                value = float(value_str)
            except ValueError:
                value = value_str  # Keep as string if conversion fails
            data_dict[key] = value
        
    return data_dict

def send_to_broker_loop_start():
    read_interval = 5  # Check for data every seconds
    try:
        while True:
            time.sleep(read_interval)
            data = receive_serial_data()
            if data:
                data = parse_data_to_dict(data)
                print(f"Received data: {data}")
                count = 1
                for type, value in data.items():
                    data_formatted = { 
                        "user_id": "VVRsnPoAEqSbUa9QLwXLgj2D9Zx2",
                        "env_id": "my_simple_garden",
                        "sensor_id": f"sensor-10{count}",
                        ##########################
                        "timestamp": str(datetime.now().astimezone()),
                        "type": type,
                        "value": value ########### always float
                    }
                    payload = json.dumps(data_formatted).encode('utf-8')
                    topic = make_topic(f'sensor-10{count}', 'data', type)
                    count += 1
                    print(f"Send data to broker: {json.dumps(data_formatted, indent=4)}")
                    send_to_broker(payload=payload, topic=topic)
                # Process the received data here
            else:
                print(f"No data received on {PORT} within the timeout.")

    except KeyboardInterrupt:
        print("Exiting serial receiver.")

if __name__ == "__main__":
    mqtt_client.loop_start()
    send_to_broker_loop_start()