package com.github.trungdung1711.kafka_client.service;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.trungdung1711.kafka_client.event.SensorData;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class SensorConsumer {

	private final ObjectMapper objectMapper = new ObjectMapper();

	private final InfluxDBService influxDBService;

	@KafkaListener(topics = {"sensor-data"})
	public void comsume(String value) {
		try {
			SensorData sensorData = objectMapper.readValue(value, SensorData.class);
			influxDBService.persistPoint(sensorData);
			
		} catch (JsonMappingException e) {
			e.printStackTrace();
		} catch (JsonProcessingException e) {
			e.printStackTrace();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
