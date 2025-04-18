from kafka import KafkaProducer
import json

from mqtt_kafka_bridge.utils.config import \
KAFKA_BOOTSTRAP_SERVER, \
    KAFKA_ENCODE_SCHEME, \
        KAFKA_BATCH_SIZE, \
            KAFKA_LINGER_TIME, \
                KAFKA_SASL_MECHANISM, \
                    KAFKA_USERNAME, \
                        KAFKA_PASSWORD, \
                            KAFKA_GROUP_ID, \
                                KAFKA_SECURITY_PROTOCOL


kafka_producer = KafkaProducer(
    bootstrap_servers = KAFKA_BOOTSTRAP_SERVER,
    key_serializer = str.encode,
    value_serializer  = lambda value : json.dumps(value).encode(KAFKA_ENCODE_SCHEME),
    linger_ms=int(KAFKA_LINGER_TIME),
    batch_size=int(KAFKA_BATCH_SIZE),
    security_protocol=KAFKA_SECURITY_PROTOCOL,
    sasl_mechanism=KAFKA_SASL_MECHANISM,
    sasl_plain_username=KAFKA_USERNAME,
    sasl_plain_password=KAFKA_PASSWORD,
    # group_id=KAFKA_GROUP_ID,
)


def kafka_connected():
    return kafka_producer.bootstrap_connected


def close_connection():
    kafka_producer.close()