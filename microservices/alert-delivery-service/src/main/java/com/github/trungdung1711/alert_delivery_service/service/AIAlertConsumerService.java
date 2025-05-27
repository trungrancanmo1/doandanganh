package com.github.trungdung1711.alert_delivery_service.service;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

import jakarta.mail.MessagingException;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@AllArgsConstructor
@Slf4j
public class AIAlertConsumerService {
	
	private EmailService emailService;

	@KafkaListener(topics = {"ai-alert"}, groupId = "alert-delivery-service", id = "alert-delivery-service1")
	public void listen(String value) throws MessagingException {
		log.info("Received this: " + value);
		emailService.sendAIAlert(null);
	}
}
