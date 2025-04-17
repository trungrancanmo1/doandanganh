import mqtt_kafka_bridge.connectors as connectors
from mqtt_kafka_bridge.utils import logger
from mqtt_kafka_bridge.utils.config import EMQX_URL, EMQX_PORT


if __name__ == "__main__":
    logger.info('Starting MQTT-to-Kafka bridge service')

    try:
        # MQTT broker
        connectors.mqtt_client.connect(host=EMQX_URL, port=int(EMQX_PORT), keepalive=60, clean_start=True)

        # Kafka bootstrap_server
        if connectors.kafka_connected():
            logger.info('Successfully connecting with the Kafka bootstrap server')
        else:
            raise ConnectionError('Fail to connect Kafka bootstrap server')
        
        # Enter the service
        logger.info('Entering the main loop of service')
        connectors.mqtt_client.loop_forever()

    except Exception as e:
        connectors.close_connection()
        logger.error(f'An error has occurred: {e}', exc_info=True)