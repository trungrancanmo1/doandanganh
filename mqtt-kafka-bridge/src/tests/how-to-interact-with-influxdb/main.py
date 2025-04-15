from influxdb_client_3 import InfluxDBClient3, Point
import time


from config.config import INFLUXDB_TOKEN, INFLUXDB_URL, INFLUXDB_ORG, INFLUXDB_BUCKET


client = InfluxDBClient3(host=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)


database="test-bucket"

data = {
  "point1": {
    "location": "Klamath",
    "species": "bees",
    "count": 23,
  },
  "point2": {
    "location": "Portland",
    "species": "ants",
    "count": 30,
  },
  "point3": {
    "location": "Klamath",
    "species": "bees",
    "count": 28,
  },
  "point4": {
    "location": "Portland",
    "species": "ants",
    "count": 32,
  },
  "point5": {
    "location": "Klamath",
    "species": "bees",
    "count": 29,
  },
  "point6": {
    "location": "Portland",
    "species": "ants",
    "count": 40,
  },
}


for key in data:
    point = (
        Point("census")
        .tag("location", data[key]["location"])
        .field(data[key]["species"], data[key]["count"])
    )
    client.write(database=database, record=point)
    time.sleep(1) # separate points by 1 second

print("Complete. Return to the InfluxDB UI.")