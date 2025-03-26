from influxdb_client_3 import InfluxDBClient3
from garden.settings import INFLUXDB


#==========================
# INFLUX DATABASE SETUP
#==========================
ifdb_client = InfluxDBClient3(
    host=INFLUXDB['host'], 
    token=INFLUXDB['token'], 
    org=INFLUXDB['org'], 
    database=INFLUXDB['bucket'])