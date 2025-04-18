import mqtt_kafka_bridge.connectors as connectors


def send_to_kafka(data : dict, topic : str):
    key = '/'.join(
        [
            data['user_id'],
            data['env_id'],
            data['sensor_id']
        ]
    )

    connectors.kafka_producer.send(
        topic=topic,
        value=data,
        key=key,
        # headers=None,
        # partition=None,
        # timestamp_ms=None   
    )