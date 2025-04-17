from kafka import KafkaProducer
import json

from mqtt_kafka_bridge.utils.config import \
KAFKA_BOOTSTRAP_SERVER, \
    KAFKA_EVENT_ENCODE_SCHEME, \
        KAFKA_BATCH_SIZE, \
            KAFKA_LINGER_TIME


kafka_producer = KafkaProducer(
    bootstrap_servers = KAFKA_BOOTSTRAP_SERVER,
    key_serializer = str.encode,
    value_serializer  = lambda value : json.dumps(value).encode(KAFKA_EVENT_ENCODE_SCHEME),
    linger_ms=int(KAFKA_LINGER_TIME),
    batch_size=int(KAFKA_BATCH_SIZE),
)


def kafka_connected():
    return kafka_producer.bootstrap_connected


def close_connection():
    kafka_producer.close()