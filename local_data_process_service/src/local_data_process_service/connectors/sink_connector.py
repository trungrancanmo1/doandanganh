from influxdb_client_3 import InfluxDBClient3
from local_data_process_service.utils import logger


from local_data_process_service.utils.config import INFLUXDB_TOKEN, INFLUXDB_URL, INFLUXDB_ORG, INFLUXDB_BUCKET


influxdb_client = InfluxDBClient3(host=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
logger.info('Connecting to InfluxDB successfully')