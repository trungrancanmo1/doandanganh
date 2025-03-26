from connectors import source_connector
from utils.logger import logger
from config.config import EMQX_URL, PORT
from phases import phase1
from phases import phase2


if __name__ == "__main__":
    logger.info('Starting MQTT client service, proceed connect with the MQTT broker')
    source_connector.client.connect(host=EMQX_URL, port=PORT, keepalive=60, clean_start=True)
    source_connector.client.loop_forever()