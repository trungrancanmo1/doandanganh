from influxdb_client_3 import InfluxDBClient3
from garden.settings import INFLUXDB


import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.enums import MQTTProtocolVersion

from garden.settings import MQTT_BROKER
from garden.settings import USER, APP_NAME


#==========================
# INFLUX DATABASE SETUP
#==========================
ifdb_client = InfluxDBClient3(
    host=INFLUXDB['host'], 
    token=INFLUXDB['token'], 
    org=INFLUXDB['org'], 
    database=INFLUXDB['bucket'])
#==========================
# INFLUX DATABASE SETUP
#==========================


#==========================
# MQTT CLIENT SETUP
#==========================
def send_command(payload : bytes, topic : str):
    try:
        mqtt_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTProtocolVersion.MQTTv5)
        mqtt_client.username_pw_set(username=MQTT_BROKER['username'], password=MQTT_BROKER['password'])
        mqtt_client.connect(host=MQTT_BROKER['url'], port=1883)

        mqtt_client.publish(topic=topic, payload=payload, qos=2)

        mqtt_client.disconnect()
    except Exception as e:
        raise IOError('MQTT service failed')
    

def make_topic(device_id : str, topic_type : str, device_type : str) -> str:
    '''
    - device_id must be in SENSOR_ID and ACTUATOR_ID
    - topic_type : 'command', 'data'
    - device_type must be in SENSOR_TYPE and ACTUATOR_TYPE

    example :
    - hcmut-smart-farm/VVRsnPoAEqSbUa9QLwXLgj2D9Zx2/my_simple_garden/actuator-103/cooler/command
    - hcmut-smart-farm/VVRsnPoAEqSbUa9QLwXLgj2D9Zx2/my_simple_garden/sensor-101/temperature/data
    '''
    topic = '/'.join (
        [
            APP_NAME,
            USER['user_id'],
            USER['env_id'],
            device_id,
            device_type,
            topic_type
        ]
    )

    # print(topic)
    return topic
#==========================
# MQTT CLIENT SETUP
#==========================