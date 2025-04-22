package config

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

type KafkaConfig struct {
	Cluster          string
	BootstrapServers []string
	Topic            string
	EncodeScheme     string
	LingerTime       time.Duration
	BatchSize        int
	SecurityProtocol string
	SASLMechanism    string
	Username         string
	Password         string
	GroupID          string
}

func LoadKafkaConfig() (*KafkaConfig, error) {
	lingerMs, err := strconv.Atoi(os.Getenv("KAFKA_LINGER_TIME"))
	if err != nil {
		return nil, fmt.Errorf("invalid KAFKA_LINGER_TIME: %w", err)
	}

	batchSize, err := strconv.Atoi(os.Getenv("KAFKA_BATCH_SIZE"))
	if err != nil {
		return nil, fmt.Errorf("invalid KAFKA_BATCH_SIZE: %w", err)
	}

	return &KafkaConfig{
		Cluster:          os.Getenv("KAFKA_CLUSTER"),
		BootstrapServers: strings.Split(os.Getenv("KAFKA_BOOTSTRAP_SERVERS"), ","),
		Topic:            os.Getenv("KAFKA_TOPIC"),
		EncodeScheme:     os.Getenv("KAFKA_ENCODE_SCHEME"),
		LingerTime:       time.Duration(lingerMs) * time.Millisecond,
		BatchSize:        batchSize,
		SecurityProtocol: os.Getenv("KAFKA_SECURITY_PROTOCOL"),
		SASLMechanism:    os.Getenv("KAFKA_SASL_MECHANISM"),
		Username:         os.Getenv("KAFKA_USERNAME"),
		Password:         os.Getenv("KAFKA_PASSWORD"),
		GroupID:          os.Getenv("KAFKA_GROUP_ID"),
	}, nil
}
