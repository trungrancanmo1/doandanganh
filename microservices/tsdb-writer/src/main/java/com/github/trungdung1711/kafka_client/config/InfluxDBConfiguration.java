package com.github.trungdung1711.kafka_client.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.influxdb.v3.client.InfluxDBClient;

@Configuration
public class InfluxDBConfiguration {
	@Value("${database.influx.host}")
	private String host;

	@Value("${database.influx.token}")
	private String token;

	@Value("${database.influx.org}")
	private String organization;

	@Value("${database.influx.bucket}")
	private String bucket;

	@Value("${database.influx.measurement}")
	private String measurement;

	@Bean
	public InfluxDBClient returInfluxDBClient() {
		return InfluxDBClient.getInstance(host, token.toCharArray(), bucket, null);
	}
}
