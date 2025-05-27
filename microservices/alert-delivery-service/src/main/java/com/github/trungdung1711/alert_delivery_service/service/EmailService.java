package com.github.trungdung1711.alert_delivery_service.service;

import org.springframework.core.io.ClassPathResource;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;

import com.github.trungdung1711.alert_delivery_service.event.AIAlert;
import com.github.trungdung1711.alert_delivery_service.event.Alert;

import jakarta.mail.MessagingException;
import jakarta.mail.internet.MimeMessage;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@AllArgsConstructor
@Slf4j
public class EmailService {

	private final JavaMailSender javaMailSender;

	public void sendDataAlert(Alert alert) throws MessagingException {
		MimeMessage message = javaMailSender.createMimeMessage();
		MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");

		helper.setFrom("hcmut-smart-farm@email.com");
		helper.setTo(alert.getMail());
		helper.setSubject("HCMUT Smart Farm System Alert");

		// HTML content with inline image reference
		String content = String.format("""
			<html>
			<body style="font-family:Arial, sans-serif; line-height:1.6;">
				<p>Dear <strong>%s</strong>,</p>

				<p>We have detected a <span style="color:red;">threshold breach</span> for one of your monitored sensors.</p>

				<ul>
					<li><strong>Location:</strong> %s</li>
					<li><strong>Sensor ID:</strong> %s</li>
					<li><strong>Current Value:</strong> %.2f</li>
					<li><strong>Timestamp:</strong> %s</li>
				</ul>

				<h4>Details:</h4>
				<ul>
					<li><strong>Sensor Type:</strong> %s</li>
					<li><strong>Minimum Threshold:</strong> %.2f</li>
					<li><strong>Maximum Threshold:</strong> %.2f</li>
				</ul>

				<p>If you need assistance, don't hesitate to reach out.</p>

				<p style="margin-top: 30px;">Best regards,<br>
				<strong>HCMUT SMART FARM Alert Service</strong></p>

				<div style="text-align: center;">
					<img src='cid:logoImage' style="max-height: 80px;" alt="Smart Farm Logo"/>
				</div>
			</body>
			</html>
			""",
			alert.getMail(),
			alert.getEnv_id(),
			alert.getSensor_id(),
			alert.getValue(),
			alert.getTimestamp(),
			alert.getType(),
			alert.getMin(),
			alert.getMax()
		);

		helper.setText(content, true);
		helper.addInline("logoImage", new ClassPathResource("static/logo.png"));

		javaMailSender.send(message);

		log.info("Successfully sent HTML mail: " + alert.getMail());
	}

	public void sendAIAlert(AIAlert aiAlert) throws MessagingException {
		MimeMessage message = javaMailSender.createMimeMessage();
		MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");

		helper.setFrom("hcmut-smart-farm@email.com");
		helper.setTo("dung.lebk2210573@hcmut.edu.vn");
		helper.setSubject("HCMUT Smart Farm System Alert");

		String content = """
			<html>
			<body style="font-family: Arial, sans-serif; line-height: 1.6;">
				<p>Dear <strong>Plant Owner</strong>,</p>

				<p>We have detected an <span style="color: red;">anomaly</span> in the health of your plant using our AI-based monitoring system.</p>

				<p>Please take a moment to inspect your plant for any visible signs of stress, disease, or abnormality.</p>

				<p>If you require assistance or have any questions, feel free to contact us anytime.</p>

				<p style="margin-top: 30px;">Best regards,<br>
				<strong>The Plant Monitoring Team<br>HCMUT Smart Farm</strong></p>

				<div style="text-align: center;">
					<img src='cid:logoImage' style="max-height: 80px;" alt="Smart Farm Logo"/>
				</div>
			</body>
			</html>
		""";

		helper.setText(content, true);
		helper.addInline("logoImage", new ClassPathResource("static/logo.png"));

		javaMailSender.send(message);
		log.info("Successfully sent AI alert HTML email");
	}
}
