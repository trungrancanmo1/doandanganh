from config import *

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.enums import MQTTProtocolVersion


mqtt_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTProtocolVersion.MQTTv5)
mqtt_client.username_pw_set(username=EMQX_USER_NAME, password=EMQX_PASSWORD)
mqtt_client.connect(host=EMQX_URL, port=1883)


# =====================================================
# CALL THIS FUNCTION TO PUBLISH THE DATA TO MQTT BROKER
# =====================================================
def send_data(payload : bytes, topic : str):
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
    print(f'Publishing data to the topic {topic} successfully')