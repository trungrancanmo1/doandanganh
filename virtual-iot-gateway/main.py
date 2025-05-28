import json
import time
import random
import logging
import os
from datetime import datetime
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.enums import MQTTProtocolVersion

from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTProtocolVersion.MQTTv5, client_id='fake-gateway', transport='tcp', reconnect_on_failure=True)
client.username_pw_set(os.getenv("EMQX_USER_NAME"), os.getenv('EMQX_PASSWORD'))
client.connect(os.getenv('EMQX_URL'), int(os.getenv('EMQX_PORT')))

logging.info("Connected to MQTT Broker")

user_id = "VVRsnPoAEqSbUa9QLwXLgj2D9Zx2"
env_id = "my_simple_garden"
sensor_ids = ["sensor-101", "sensor-102", "sensor-103"]
sensors = ["temperature", "humidity", "light"]

logging.info("Prepared data to send")
logging.info("Entered loop")

while True:
    for index, sensor_id in enumerate(sensor_ids):
        value = round(random.random() * 100, 2)  # random float [0, 100) with 2 decimals

        data_point = {
            "user_id": user_id,
            "env_id": env_id,
            "sensor_id": sensor_id,
            "timestamp": str(datetime.now().astimezone()),
            "type": sensors[index],
            "value": value,
            "state": 0
        }

        try:
            json_bytes = json.dumps(data_point).encode('utf-8')
        except Exception as e:
            logging.error(f"Error serializing JSON: {e}")
            continue

        topic = "/".join([
            os.getenv("MAIN_APP"),
            data_point["user_id"],
            data_point["env_id"],
            data_point["sensor_id"],
            data_point["type"],
            "data"
        ])

        client.publish(topic, payload=json_bytes, qos=0)
        logging.info(f"Sent fake data to Broker")

    time.sleep(20)