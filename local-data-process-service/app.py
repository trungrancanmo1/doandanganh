from connectors import source_connector
from utils.logger import logger
from config.config import EMQX_URL, PORT
from phases import phase1
# from phases import phase2


if __name__ == "__main__":
    logger.info('Starting MQTT client service, proceed connect with the MQTT broker')
    try:
        source_connector.mqtt_client.connect(host=EMQX_URL, port=PORT, keepalive=60, clean_start=True)
        source_connector.mqtt_client.loop_forever()
    except Exception as e:
        logger.error(f'An error has occurred: {e}', exc_info=True)