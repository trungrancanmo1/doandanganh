package com.github.trungdung1711.alert_delivery_service.service;

import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

import com.github.trungdung1711.alert_delivery_service.event.AIAlert;
import com.github.trungdung1711.alert_delivery_service.event.Alert;

import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@AllArgsConstructor
@Slf4j
public class EmailService {

	private final JavaMailSender javaMailSender;

	public void sendDataAlert(Alert alert) {
		SimpleMailMessage message = new SimpleMailMessage();
	
		message.setFrom("your@email.com");
		message.setTo(alert.getMail());
		message.setSubject("HCMUT Smart Farm System");
	
		String content = String.format("""
				Dear %s User,
	
				We have detected a threshold breach for one of your monitored sensors.
	
				📍 **Location**: %s
				🔍 **Sensor ID**: %s
				📊 **Current Value**: %.2f
				🔺 **Threshold**: %.2f
				🕒 **Timestamp**: %s
	
				The sensor value has exceeded the defined threshold. Please take immediate action to investigate the issue.
	
				**Details:**
				- Sensor Type: %s
				- Minimum Threshold: %.2f
				- Maximum Threshold: %.2f
	
				If you need assistance, don't hesitate to reach out.
	
				Best regards,
				HCMUT SMART FARM Alert Service
				""",
				alert.getUser_id(),
				alert.getEnv_id(),
				alert.getSensor_id(),
				alert.getValue(),
				alert.getMax(),
				alert.getTimestamp(),
				alert.getType(),
				alert.getMin(),
				alert.getMax()
		);
	
		message.setText(content);
	
		javaMailSender.send(message);
	
		log.info("Successfully sent data alert email to: " + alert.getMail());
	}	

	public void sendAIAlert(AIAlert aiAlert) {
		SimpleMailMessage message = new SimpleMailMessage();
	
		message.setFrom("your@email.com");
		message.setTo("dung.lebk2210573@hcmut.edu.vn");
		message.setSubject("HCMUT Smart Farm System");
	
		String content = "Dear Plant Owner,\n\n"
				+ "We have detected an anomaly in the health of your plant. Please take a moment to inspect your plant for any potential issues.\n\n"
				+ "If you require assistance, feel free to reach out to us.\n\n"
				+ "Best regards,\n"
				+ "The Plant Monitoring Team";
	
		message.setText(content);
	
		javaMailSender.send(message);
		log.info("Successfully sent AI alert email");
	}
}
