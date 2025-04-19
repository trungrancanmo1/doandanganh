package main

import (
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/confluentinc/confluent-kafka-go/v2/kafka"
	"github.com/gorilla/websocket"
	"github.com/joho/godotenv"
)

func main() {
	// load env
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Unable to load .env")
	}

	// create config
	config := LoadConfig()
	fmt.Println(config.BootstrapServer)
	// http.HandleFunc("/ws", wsEndpoint)
	// log.Fatal(http.ListenAndServe(":8080", nil))

	// Kafka consumer
	kafkaConfig := &kafka.ConfigMap{
		"bootstrap.servers": config.BootstrapServer,
		"security.protocol": config.SecurityProtocol,
		"sasl.mechanisms":   config.SaslMechanism,
		"sasl.username":     config.Username,
		"sasl.password":     config.Password,
		"group.id":          config.GroupId,
	}
	c, err := kafka.NewConsumer(kafkaConfig)
	if err != nil {
		log.Fatal("Failed to create a Kafka consumer")
	}

	// Subscribe for topic
	err = c.Subscribe(config.Topic, nil)
	if err != nil {
		log.Fatal("Failed to subscribe the topic")
	}

	// Now run
	for {
		// infinitely block
		message, err := c.ReadMessage(-1)
		if err != nil {
			log.Fatal("Received error not message")
		}
		fmt.Println("Received message" + message.String())
	}
}

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin:     func(r *http.Request) bool { return true },
}

func handler(writer http.ResponseWriter, request *http.Request) {
	writer.WriteHeader(200)
	message := "Hello, World!"
	encodedMessage := []byte(message)
	value, err := writer.Write(encodedMessage)
	if err != nil {
		fmt.Println("Error response")
	}
	fmt.Println(value)
}

func wsEndpoint(w http.ResponseWriter, r *http.Request) {
	log.Println("New connection attempt")

	// Upgrading
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println(err)
		return
	}
	defer ws.Close()

	log.Println("Client Connected")

	// Listening
	for {
		// Reading
		messageType, msg, err := ws.ReadMessage()
		if err != nil {
			log.Println("Read error:", err)
			break
		}

		log.Printf("Received: %s", msg)

		// Sending back
		if err := ws.WriteMessage(messageType, msg); err != nil {
			log.Println("Write error:", err)
			break
		}
	}

	log.Println("Client disconnected")
}

type Config struct {
	Cluster          string
	BootstrapServer  string
	Topic            string
	EncodeScheme     string
	LingerTime       string
	BatchSize        string
	SecurityProtocol string
	SaslMechanism    string
	Username         string
	Password         string
	GroupId          string
}

func LoadConfig() *Config {
	return &Config{
		Cluster:          os.Getenv("KAFKA_CLUSTER"),
		BootstrapServer:  os.Getenv("KAFKA_BOOTSTRAP_SERVER"),
		Topic:            os.Getenv("KAFKA_TOPIC"),
		EncodeScheme:     os.Getenv("KAFKA_ENCODE_SCHEME"),
		LingerTime:       os.Getenv("KAFKA_LINGER_TIME"),
		BatchSize:        os.Getenv("KAFKA_BATCH_SIZE"),
		SecurityProtocol: os.Getenv("KAFKA_SECURITY_PROTOCOL"),
		SaslMechanism:    os.Getenv("KAFKA_SASL_MECHANISM"),
		Username:         os.Getenv("KAFKA_USERNAME"),
		Password:         os.Getenv("KAFKA_PASSWORD"),
		GroupId:          os.Getenv("KAFKA_GROUP_ID"),
	}
}
