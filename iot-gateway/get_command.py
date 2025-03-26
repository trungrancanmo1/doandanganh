import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.enums import MQTTProtocolVersion
import json



TOPIC = '#'
EMQX_USER_NAME='test-flow'
EMQX_PASSWORD='Trungdung1711'
EMQX_URL='z7f54af0.ala.dedicated.aws.emqxcloud.com'


def on_connect(mqttc, obj, flags, rc, properties):
    mqttc.subscribe(topic=TOPIC)


# =================================================
# ON_MESSAGE CALL-BACK
# =================================================
def on_message(mqttc, obj, msg):

    # decode the payload
    data = json.loads(msg.payload.decode('utf-8'))

    # control device

    print(data)
    


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