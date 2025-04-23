package com.github.trungdung1711.alert_delivery_service.service;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@AllArgsConstructor
@Slf4j
public class AIAlertConsumerService {
	
	private EmailService emailService;

	@KafkaListener(topics = {"ai-alert"}, groupId = "alert-delivery-service", id = "alert-delivery-service1")
	public void listen(String value) {
		// skip for now
		// AIAlert aiAlert = objectMapper.readValue(value, AIAlert.class);
		log.info("Received this: " + value);
		emailService.sendAIAlert(null);
	}
}
