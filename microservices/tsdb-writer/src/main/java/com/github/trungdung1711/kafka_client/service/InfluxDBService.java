package com.github.trungdung1711.kafka_client.service;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import com.github.trungdung1711.kafka_client.event.SensorData;
import com.influxdb.v3.client.InfluxDBClient;
import com.influxdb.v3.client.Point;
import com.influxdb.v3.client.write.WriteOptions;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class InfluxDBService {
	@Value("${database.influx.measurement}")
	private String measurement;

	@Value("${database.influx.bucket}")
	private String bucket;

	private final InfluxDBClient influxDBClient;

	public void persistPoint(SensorData sensorData) {
		Map<String, String> tags = new HashMap<String, String>();
		tags.put("user_id", sensorData.getUser_id());
		tags.put("env_id", sensorData.getEnv_id());
		tags.put("sensor_id", sensorData.getSensor_id());
		tags.put("type", sensorData.getType());

		Point point = Point
			.measurement(measurement)
			.setTags(tags)
			.setFloatField("value", sensorData.getValue())
			.setTimestamp(Instant.now());
		
		influxDBClient.writePoint(point, new WriteOptions.Builder().database(bucket).build());
		log.info("Successfully persisting the data to the database");
	}
}
