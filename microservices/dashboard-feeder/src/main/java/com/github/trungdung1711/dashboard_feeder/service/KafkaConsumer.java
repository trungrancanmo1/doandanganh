package com.github.trungdung1711.dashboard_feeder.service;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.core.JsonProcessingException;
import lombok.AllArgsConstructor;

@AllArgsConstructor
@Service
public class KafkaConsumer {
	private SimpMessagingTemplate messagingTemplate;
	@KafkaListener(topics = {"sensor-data"})
	public void listen(String value) throws Exception, JsonProcessingException {
		System.out.println("Received: " + value);
		messagingTemplate.convertAndSend("/topic/sensor", value);
	}
}
