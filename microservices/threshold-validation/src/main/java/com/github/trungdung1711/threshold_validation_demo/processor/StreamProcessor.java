package com.github.trungdung1711.threshold_validation_demo.processor;

import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.KTable;
import org.apache.kafka.streams.kstream.Predicate;
import org.apache.kafka.streams.kstream.Produced;
import org.apache.kafka.streams.kstream.ValueJoiner;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafkaStreams;

import com.github.trungdung1711.threshold_validation_demo.event.Alert;
import com.github.trungdung1711.threshold_validation_demo.event.SensorData;
import com.github.trungdung1711.threshold_validation_demo.event.ThresHoldData;

import lombok.extern.slf4j.Slf4j;

@Configuration
@Slf4j
@EnableKafkaStreams
public class StreamProcessor {
	@Value("${spring.kafka.streams.properties.data-topic}")
	private String dataTopic;

	@Value("${spring.kafka.streams.properties.threshold-topic}")
	private String thresholdTopic;

	@Value("${spring.kafka.streams.properties.alerts-topic}")
	private String alertTopic;

	@Bean
	public KStream<String, Alert> kStream(
		Serde<SensorData> serdeSensorData,
		Serde<ThresHoldData> serdeThresHoldData,
		Serde<Alert> serdeAlert,
		StreamsBuilder streamsBuilder
	) {
		/*
		 * KStream for sensor_data
		 */
		KStream<String, SensorData> sensorKStream = streamsBuilder.stream(dataTopic, Consumed.with(Serdes.String(), serdeSensorData));

		/*
		 * KTable for threshold_config
		 */
		KTable<String, ThresHoldData> thresholdKTable = streamsBuilder.table(thresholdTopic, Consumed.with(Serdes.String(), serdeThresHoldData));

		/*
		 * Defining the topology, KStream for threshold_alerts
		 */
		KStream<String, Alert> alertKStream = sensorKStream.leftJoin(thresholdKTable, new ValueJoiner<SensorData, ThresHoldData, Alert>() {

			@Override
			public Alert apply(SensorData sensorData, ThresHoldData thresHoldData) {
				/*
				 * Joined
				 */
				if (thresHoldData == null || sensorData == null) {
					log.info("One of the data is null");
					return null;
				}

				double value = sensorData.getValue();
				double min = thresHoldData.getMin();
				double max = thresHoldData.getMax();
				if (value < min || value > max) {
					/*
					 * threshold violated
					 */
					log.info("Threshold violated with value: " + value + ", min: " + min + ", max: " + max);
					return Alert.builder()
								.user_id(sensorData.getUser_id())
								.env_id(sensorData.getEnv_id())
								.sensor_id(sensorData.getSensor_id())
								.timestamp(sensorData.getTimestamp())
								.type(sensorData.getType())
								.max(thresHoldData.getMax())
								.min(thresHoldData.getMin())
								.value(sensorData.getValue())
								.mail(thresHoldData.getMail())
								.build();
				}
				return null;
			}
		});

		alertKStream.filter(new Predicate<String,Alert>() {

			@Override
			public boolean test(String key, Alert value) {
				return value != null;
			}
			
		})
		.to(alertTopic, Produced.with(Serdes.String(), serdeAlert));

		return alertKStream;
	}
}
