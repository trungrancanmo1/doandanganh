import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.enums import MQTTProtocolVersion
import json

from local_data_process_service.utils import logger
from local_data_process_service.utils.config import TOPIC, EMQX_USER_NAME, EMQX_PASSWORD, EMQX_URL, DATA_ENCODE_SCHEME
from local_data_process_service.core.phases import phase1


def on_connect(mqttc, obj, flags, rc, properties):
    logger.info(msg='Successfully connect to the MQTT broker remotely')
    mqttc.subscribe(topic=TOPIC)


# =================================================
# ON_MESSAGE CALL-BACK
# =================================================
def on_message(mqttc, obj, msg):
    logger.info('Putting task and data into Redis')

    # decode the payload
    data = {
        'data' : json.loads(msg.payload.decode(DATA_ENCODE_SCHEME)),
        'topic' : msg.topic
    }

    phase1.delay(data)
    


def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
    logger.info("Subscribed: " + str(mid) + " " + str(reason_code_list))


def on_log(mqttc, obj, level, string):
    print(string)


mqtt_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTProtocolVersion.MQTTv5)
mqtt_client.username_pw_set(username=EMQX_USER_NAME, password=EMQX_PASSWORD)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message