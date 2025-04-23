package com.github.trungdung1711.dashboard_feeder.service;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.stereotype.Service;
import java.util.Properties;

@Service
public class KafkaProducerService {
    private KafkaProducer<String, String> producer;
    private static final String TOPIC = "sensor-data";  // Topic bạn muốn gửi tin nhắn vào.

    public KafkaProducerService() {
        // Cấu hình Kafka producer
        Properties properties = new Properties();
        properties.put("bootstrap.servers", "localhost:9092");  // Kafka broker.
        properties.put("key.serializer", StringSerializer.class.getName());
        properties.put("value.serializer", StringSerializer.class.getName());
        producer = new KafkaProducer<>(properties);
    }

    public void sendMessage(String message) {
        // Tạo ProducerRecord và gửi tin nhắn vào topic
        ProducerRecord<String, String> record = new ProducerRecord<>(TOPIC, message);
        producer.send(record, (metadata, exception) -> {
            if (exception != null) {
                exception.printStackTrace();
            } else {
                System.out.println("Message sent to topic: " + metadata.topic() + " with offset: " + metadata.offset());
            }
        });
    }

    public void close() {
        producer.close();
    }
}
