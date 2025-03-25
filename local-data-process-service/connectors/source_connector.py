import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.enums import MQTTProtocolVersion


from utils.logger import logger
from config.config import TOPIC, EMQX_USER_NAME, EMQX_PASSWORD, EMQX_URL, DATA_DECODE
from phases import phase1


def on_connect(mqttc, obj, flags, rc, properties):
    logger.info(msg='Successfully connect to the MQTT broker remotely')
    mqttc.subscribe(topic=TOPIC)


# =================================================
# ON_MESSAGE CALL-BACK
# =================================================
def on_message(mqttc, obj, msg):
    # payload = json.loads(msg.payload.decode(DATA_DECODE))
    # create and add the data to the redis
    # and return to handle the next message
    
    # put task into redis
    logger.info('Putting task into Redis')
    phase1.delay(msg.payload.decode(DATA_DECODE))
    


def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
    logger.info("Subscribed: " + str(mid) + " " + str(reason_code_list))


def on_log(mqttc, obj, level, string):
    print(string)


client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTProtocolVersion.MQTTv5)
client.username_pw_set(username=EMQX_USER_NAME, password=EMQX_PASSWORD)

client.on_connect = on_connect
client.on_message = on_message