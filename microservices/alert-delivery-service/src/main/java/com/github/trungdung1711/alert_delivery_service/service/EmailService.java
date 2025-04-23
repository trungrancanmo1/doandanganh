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
        message.setSubject("🚨 Alert: Threshold Breached");

        String content = String.format("""
                Dear User,

                A threshold breach has been detected!

                🔍 Sensor ID: %s
                📍 Location: %s
                📊 Value: %.2f
                🔺 Threshold: %.2f
                🕒 Timestamp: %s
                    Max: %.2f
                    Min: %.2f

                Please investigate this alert as soon as possible.

                Regards,
                HCMUT SMART FARM Alert Service
                """,
                alert.getSensor_id(),
                alert.getEnv_id(),
                alert.getValue(),
                alert.getValue(),
                alert.getTimestamp(),
                alert.getMax(),
                alert.getMin()
        );

        message.setText(content);

        javaMailSender.send(message);

        log.info("Successfully send email to: " + alert.getMail());
    }

    public void sendAIAlert(AIAlert aiAlert) {
        
        SimpleMailMessage message = new SimpleMailMessage();

        message.setFrom("your@email.com");
        message.setTo("dung.lebk2210573@hcmut.edu.vn");
        message.setSubject("🚨 Pest alert");

        String content = "There is something weird with your plant, please check it out";

        message.setText(content);

        javaMailSender.send(message);
        log.info("Successfully send AI email");
    }
}
