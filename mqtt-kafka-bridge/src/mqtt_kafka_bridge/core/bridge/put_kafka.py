import mqtt_kafka_bridge.connectors as connectors


def send_to_kafka(data : dict, topic : str):
    connectors.kafka_producer.send(
        topic=topic,
        value=data,
        key=data['sensor_id'],
        # headers=None,
        # partition=None,
        # timestamp_ms=None   
    )