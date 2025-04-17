import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.enums import MQTTProtocolVersion
import json

from mqtt_kafka_bridge.utils import logger
from mqtt_kafka_bridge.utils.config import TOPIC, EMQX_USER_NAME, EMQX_PASSWORD, EMQX_URL, DATA_ENCODE_SCHEME, KAFKA_TOPIC
from mqtt_kafka_bridge.core.bridge import send_to_kafka


def on_connect(mqttc, obj, flags, rc, properties):
    logger.info(msg='Successfully connecting to the MQTT broker')
    mqttc.subscribe(topic=TOPIC)


# =================================================
# ON_MESSAGE CALL-BACK
# =================================================
def on_message(mqttc, obj, msg):
    # logger.info('Putting task and data into Redis')

    # decode the payload
    data = {
        'data' : json.loads(msg.payload.decode(DATA_ENCODE_SCHEME)),
        'topic' : msg.topic
    }

    # publish to Kafka topic
    # asynchronous send and automatic push
    send_to_kafka(data['data'], KAFKA_TOPIC)
    logger.info('Successfully pubishing event to Kafka')


def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
    logger.info("Subscribed: " + str(mid) + " " + str(reason_code_list))


def on_log(mqttc, obj, level, string):
    print(string)


mqtt_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTProtocolVersion.MQTTv5)
mqtt_client.username_pw_set(username=EMQX_USER_NAME, password=EMQX_PASSWORD)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message