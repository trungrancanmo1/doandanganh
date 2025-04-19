package redpd

import (
	"log"
	"time"

	"github.com/confluentinc/confluent-kafka-go/v2/kafka"
	"github.com/trungdung1711/realtime-service/config"
)

type RedpandaConsumer struct {
	Client *kafka.Consumer
	Config *config.KafkaConfig
}

type Message struct {
	data  *SensorData
	key   []byte
	value []byte
}

func (m *Message) Data() *SensorData {
	return m.data
}

func (m *Message) Value() []byte {
	return m.value
}

func NewSensorMessage(m *kafka.Message) *Message {
	msg := Message{}
	msg.key = m.Key
	msg.value = m.Value
	return &msg
}

type SensorData struct {
	UserId    string  `json:"user_id"`
	EnvId     string  `json:"env_id"`
	SensorId  string  `json:"sensor_id"`
	Timestamp string  `json:"timestamp"`
	Type      string  `json:"type"`
	Value     float64 `json:"value"`
	State     int     `json:"state"`
}

func NewRedpandaConsumer(config *config.KafkaConfig) *RedpandaConsumer {
	kafkaConfig := &kafka.ConfigMap{
		"bootstrap.servers": config.BootstrapServers[0],
		"security.protocol": config.SecurityProtocol,
		"sasl.mechanisms":   config.SASLMechanism,
		"sasl.username":     config.Username,
		"sasl.password":     config.Password,
		"group.id":          config.GroupID,
	}
	c, err := kafka.NewConsumer(kafkaConfig)
	if err != nil {
		log.Fatal("Fail to create a consumer")
	}
	return &RedpandaConsumer{Client: c, Config: config}
}

func (c *RedpandaConsumer) Read() *Message {
	for {
		msg, err := c.Client.ReadMessage(-1)
		if err != nil {
			log.Printf("Kafka read error: %v\n", err)
			time.Sleep(time.Second * 5)
			continue
		}

		return NewSensorMessage(msg)
	}
}

func (c *RedpandaConsumer) Subscribe(t string) {
	err := c.Client.Subscribe(t, nil)
	if err != nil {
		log.Fatalf("Fail to subscribe topic %s\n", t)
	}
}

func (c *RedpandaConsumer) Start(msg chan *Message) error {
	c.Subscribe(c.Config.Topic)
	log.Println("Connected to Kafka")
	for {
		message := c.Read()
		log.Println("Received a data from Kafka")
		msg <- message
	}
}
