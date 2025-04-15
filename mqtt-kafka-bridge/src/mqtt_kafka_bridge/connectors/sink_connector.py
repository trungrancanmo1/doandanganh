from influxdb_client_3 import InfluxDBClient3
from mqtt_kafka_bridge.utils import logger


from mqtt_kafka_bridge.utils.config import INFLUXDB_TOKEN, INFLUXDB_URL, INFLUXDB_ORG, INFLUXDB_BUCKET


influxdb_client = InfluxDBClient3(host=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
logger.info('Connecting to InfluxDB successfully')