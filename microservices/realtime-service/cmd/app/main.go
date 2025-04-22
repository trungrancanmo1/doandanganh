package main

import (
	"log"

	"github.com/trungdung1711/realtime-service/config"
	"github.com/trungdung1711/realtime-service/internal/auth"
	"github.com/trungdung1711/realtime-service/internal/realtime"
	"github.com/trungdung1711/realtime-service/internal/redpd"
)

func main() {
	// load env
	// err := godotenv.Load()
	// if err != nil {
	// 	log.Fatalln("Unable to load .env")
	// }

	kafkaConfig, err := config.LoadKafkaConfig()
	if err != nil {
		log.Fatalln("Fail to load kafka configuration")
	}

	jwtConfig, err := config.LoadJwtConfig()
	if err != nil {
		log.Fatalln("Fail to load jwt secret key")
	}

	// Dependency injection
	// Kafka
	c := redpd.NewRedpandaConsumer(kafkaConfig)

	// Validator
	v := auth.NewJwtValidator(jwtConfig.SecretKey)

	// Websocket
	s := realtime.NewWebsocketServer(v)

	// Starting
	go c.Start(s.Hub.Message)
	s.Run()
}
