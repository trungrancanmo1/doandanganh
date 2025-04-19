package realtime

import (
	"log"
	"net/http"
	"time"

	"github.com/gorilla/websocket"
	"github.com/trungdung1711/realtime-service/internal/auth"
	"github.com/trungdung1711/realtime-service/internal/redpd"
)

type Client struct {
	ID   string
	Conn *websocket.Conn
	Send chan []byte
}

type Hub struct {
	Clients    map[string]*Client
	Register   chan *Client
	Unregister chan *Client
	Broadcast  chan []byte
	Message    chan *redpd.Message
}

func (h *Hub) Run() {
	for {
		select {
		case client := <-h.Register:
			h.Clients[client.ID] = client

		case client := <-h.Unregister:
			delete(h.Clients, client.ID)

		case msg := <-h.Broadcast:
			log.Println(msg)

		case msg := <-h.Message:
			if len(h.Clients) == 0 {
				log.Println("There is no client connected")
				continue
			}
			// Assume only 1
			client := h.Clients["test@email.com"]
			client.Send <- msg.Value()
		}
	}
}

func NewClient(id string, conn *websocket.Conn) *Client {
	return &Client{
		ID:   id,
		Conn: conn,
		Send: make(chan []byte, 256),
	}
}

type Server interface {
	Run()
}

type WebsockerServer struct {
	Upgrader  websocket.Upgrader
	Validator auth.Validator
	Hub       *Hub
}

func (w *WebsockerServer) ping(conn *websocket.Conn) {
	ticker := time.NewTicker(5 * time.Second)
	defer ticker.Stop()

	for {
		<-ticker.C
		err := conn.WriteMessage(websocket.PingMessage, nil)
		if err != nil {
			log.Println("Ping fail!")
			return
		}
	}
}

func NewWebsocketServer(validator auth.Validator) *WebsockerServer {
	return &WebsockerServer{
		Upgrader: websocket.Upgrader{
			ReadBufferSize:  1024,
			WriteBufferSize: 1024,
			CheckOrigin: func(r *http.Request) bool {
				return true
			},
		},
		Validator: validator,
		Hub: &Hub{
			Clients:    make(map[string]*Client),
			Register:   make(chan *Client, 256),
			Unregister: make(chan *Client),
			Broadcast:  make(chan []byte),
			Message:    make(chan *redpd.Message, 256),
		},
	}
}

func (s *WebsockerServer) Run() {
	// 1. Run the Hub?
	go s.Hub.Run()

	http.HandleFunc("/ws", func(w http.ResponseWriter, r *http.Request) {
		// 1. Extract the token from the URL query parameter
		token := r.URL.Query().Get("token")
		if token == "" {
			http.Error(w, "Token is required", http.StatusBadRequest)
			return
		}

		// 2. Validate the token
		claims, err := s.Validator.Validate(token)
		if err != nil {
			http.Error(w, "Token is invalid", http.StatusUnauthorized)
			return
		}

		// 3. Upgrade the connection to WebSocket
		conn, err := s.Upgrader.Upgrade(w, r, nil)
		if err != nil {
			http.Error(w, "Unable to upgrade to websocket protocol", http.StatusServiceUnavailable)
			return
		}
		defer conn.Close()

		// 4. Extract email from token claims
		email, ok := claims["email"].(string)
		if !ok {
			http.Error(w, "Invalid token claims", http.StatusUnauthorized)
			return
		}

		// 5. Create a new client and register it
		client := NewClient(email, conn)
		s.Hub.Register <- client

		// 6. Start pinging the client
		go s.ping(conn)

		// 7. Handle outgoing messages to the client
		for msg := range client.Send {
			if err := conn.WriteMessage(websocket.TextMessage, msg); err != nil {
				log.Println("Error writing to WebSocket:", err)
				s.Hub.Unregister <- client
				return
			}
		}

		// 8. Unregister the client when disconnected
		s.Hub.Unregister <- client
	})

	log.Println("Service listening at port 8080")
	log.Fatalln(http.ListenAndServe(":8080", nil))
}
