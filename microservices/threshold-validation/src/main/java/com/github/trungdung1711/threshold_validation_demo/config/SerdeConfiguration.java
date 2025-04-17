package com.github.trungdung1711.threshold_validation_demo.config;

import org.apache.kafka.common.serialization.Serde;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.support.serializer.JsonSerde;

import com.github.trungdung1711.threshold_validation_demo.event.Alert;
import com.github.trungdung1711.threshold_validation_demo.event.SensorData;
import com.github.trungdung1711.threshold_validation_demo.event.ThresHoldData;

@Configuration
public class SerdeConfiguration {
	@Bean
	public Serde<SensorData> sensorDataSerde() {
		return new JsonSerde<>(SensorData.class);
	}

	@Bean
	public Serde<ThresHoldData> thresholdDataSerde() {
		return new JsonSerde<>(ThresHoldData.class);
	}

	@Bean
	public Serde<Alert> alertSerde() {
		return new JsonSerde<>(Alert.class);
	}
}
