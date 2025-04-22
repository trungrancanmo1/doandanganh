package interfaces

import "github.com/trungdung1711/realtime-service/internal/redpd"

type Consumer interface {
	Read() *redpd.Message
	Subscribe(t string)
	Start(msg chan *redpd.Message) error
}
