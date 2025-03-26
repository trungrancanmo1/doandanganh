from celery.utils.log import get_task_logger
from influxdb_client_3 import Point

from capp import celery
from config.config import DATA_ENCODE_SCHEME, MEASUREMENT, INFLUXDB_BUCKET
from connectors.sink_connector import influxdb_client


logger = get_task_logger(__name__)


# =================================================
# PHASE 1 TASK: PERSIST TO THE DATABASE
# =================================================
@celery.task(name='phases.phase1')
def phase1(data):
    logger.info('Starting Phase 1...')
    payload_dict = data['data']
    topic = data['topic']

    # InfluxDB persisitence
    point = (
                Point(MEASUREMENT) 
                .tag(key='user_id', value=payload_dict['user_id']) 
                .tag(key='env_id', value=payload_dict['env_id'])
                .tag(key='sensor_id', value=payload_dict['sensor_id'])
                .tag(key='type', value=payload_dict['type'])
                .field(field='value', value=payload_dict['value'])
                .time(time=payload_dict['timestamp'])
            )
    
    influxdb_client.write(database=INFLUXDB_BUCKET, record=point)

    logger.info('Finished Phase 1.')


# =================================================
# MESSAGE FORM IN JSON
# =================================================
# message = {
#     "user_id" : "VVRsnPoAEqSbUa9QLwXLgj2D9Zx2",
#     "env_id" : "my_simple_garden",
#     "sensor_id" : "sensor_101",
#     "timestamp" : "2024-03-25T12:05:00Z",
#     "type" : "temperature", # humid/light
#     "value" : 35.36,
#     # "unit" : "",
# }