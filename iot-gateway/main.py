from config import make_topic
from iot_gateway_to_mqtt_broker import send_to_broker

from datetime import datetime
import json


if __name__ == '__main__':
    topic = make_topic('sensor-101', 'data', 'temperature')

    sample_data =  { 
        "user_id": "VVRsnPoAEqSbUa9QLwXLgj2D9Zx2",
        "env_id": "my_simple_garden",
        "sensor_id": "sensor-101",
        ##########################
        "timestamp": str(datetime.now().astimezone()),
        "type": "temperature",
        "value": 40.1 ########### always float
        }
    
    payload = json.dumps(sample_data).encode('utf-8')

    send_to_broker(payload=payload, topic=topic)