package com.github.trungdung1711.kafka_client.service;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
public class TestConsumer {
	@KafkaListener(topics = {"demo-alerts"})
	public void listen(String message) {
		System.out.println("Message received: " + message);
	}
}
