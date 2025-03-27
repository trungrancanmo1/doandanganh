from local_data_process_service.connectors import source_connector
from local_data_process_service.utils import logger
from local_data_process_service.utils.config import EMQX_URL, EMQX_PORT
from local_data_process_service.core.phases import phase1
# from phases import phase2


if __name__ == "__main__":
    logger.info('Starting MQTT client service, proceed connect with the MQTT broker')
    try:
        source_connector.mqtt_client.connect(host=EMQX_URL, port=int(EMQX_PORT), keepalive=60, clean_start=True)
        source_connector.mqtt_client.loop_forever()
    except Exception as e:
        logger.error(f'An error has occurred: {e}', exc_info=True)