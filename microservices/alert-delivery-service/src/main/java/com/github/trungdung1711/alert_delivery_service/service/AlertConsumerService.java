package com.github.trungdung1711.alert_delivery_service.service;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.trungdung1711.alert_delivery_service.event.Alert;

import lombok.AllArgsConstructor;

@Service
@AllArgsConstructor
public class AlertConsumerService {
	private final ObjectMapper objectMapper = new ObjectMapper();

	private final EmailService emailService;

	@KafkaListener(topics = {"alert"}, groupId = "alert-delivery-service", id = "alert-delivery-service")
	public void listen(String value) {
		try {
			Alert alert = objectMapper.readValue(value, Alert.class);
			
			emailService.sendDataAlert(alert);
		} catch (JsonMappingException e) {
			e.printStackTrace();
		} catch (JsonProcessingException e) {
			e.printStackTrace();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
