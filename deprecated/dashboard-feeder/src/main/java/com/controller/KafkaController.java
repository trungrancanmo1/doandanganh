package com.github.trungdung1711.dashboard_feeder.controller;

import com.github.trungdung1711.dashboard_feeder.service.KafkaProducerService;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class KafkaController {

    private final KafkaProducerService kafkaProducerService;

    public KafkaController(KafkaProducerService kafkaProducerService) {
        this.kafkaProducerService = kafkaProducerService;
    }

    // POST endpoint để gửi tin nhắn vào Kafka
    @PostMapping("/send-message")
    public String sendMessage(@RequestBody String message) {
        kafkaProducerService.sendMessage(message);
        return "Message sent to Kafka topic";
    }
}
