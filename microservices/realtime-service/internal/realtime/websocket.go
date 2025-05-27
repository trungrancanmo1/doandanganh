package realtime

import (
	"log"
	"net/http"
	"time"

	"github.com/gorilla/websocket"
	"github.com/trungdung1711/realtime-service/internal/auth"
	"github.com/trungdung1711/realtime-service/internal/redpd"
)

const (
	pongWait   = 60 * time.Second
	pingPeriod = (pongWait * 9) / 10
	writeWait  = 10 * time.Second
)

type Client struct {
	ID   string
	Conn *websocket.Conn
	Send chan []byte
	Hub  *Hub
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
			// if there is another client
			// overwrite that value
			log.Println("New client enters")
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
			// We have to choose which one
			// to give the data to client
			client := h.Clients["ngynhogminh@gmail.com"]
			client.Send <- msg.Value()
		}
	}
}

func NewClient(id string, conn *websocket.Conn, hub *Hub) *Client {
	return &Client{
		ID:   id,
		Conn: conn,
		Send: make(chan []byte, 256),
		Hub:  hub,
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
			Unregister: make(chan *Client, 256),
			Broadcast:  make(chan []byte),
			Message:    make(chan *redpd.Message, 256),
		},
	}
}

func (s *WebsockerServer) Run() {
	// 1. Run the Hub?
	go s.Hub.Run()

	http.HandleFunc("/ws", func(w http.ResponseWriter, r *http.Request) {
		log.Println("New connection")
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
		// defer conn.Close()

		// 4. Extract email from token claims
		email, ok := claims["email"].(string)
		if !ok {
			http.Error(w, "Invalid token claims", http.StatusUnauthorized)
			return
		}

		// 5. Create a new client and register it
		client := NewClient(email, conn, s.Hub)
		s.Hub.Register <- client

		go client.WritePump()
		go client.ReadPump()
	})

	log.Println("Service listening at port 8080")
	log.Fatalln(http.ListenAndServe(":8080", nil))
}

func (c *Client) WritePump() {
	ticker := time.NewTicker(pingPeriod)
	defer func() {
		ticker.Stop()
		c.Conn.Close()
		log.Println("Write close")
	}()

	for {
		// listen on channel
		select {
		case <-ticker.C:
			// ping
			c.Conn.SetWriteDeadline(time.Now().Add(writeWait))

			log.Println("Ping sent")
			if err := c.Conn.WriteMessage(websocket.PingMessage, nil); err != nil {
				return
			}

		case message, ok := <-c.Send:
			// new data to serve
			log.Println("Sent to dashboard")
			c.Conn.SetWriteDeadline(time.Now().Add(writeWait))
			if !ok {
				c.Conn.WriteMessage(websocket.CloseMessage, []byte{})
				return
			}

			if err := c.Conn.WriteMessage(websocket.TextMessage, message); err != nil {
				// write error
				return
			}
		}
	}
}

func (c *Client) ReadPump() {
	defer func() {
		c.Hub.Unregister <- c
		c.Conn.Close()
		log.Println("Read close")
	}()

	c.Conn.SetReadLimit(512)
	c.Conn.SetReadDeadline(time.Now().Add(pongWait))
	c.Conn.SetPongHandler(func(appData string) error {
		c.Conn.SetReadDeadline(time.Now().Add(pongWait))
		log.Println("Received pong")
		return nil
	})

	// Enter the read loop
	for {
		_, _, err := c.Conn.ReadMessage()
		if err != nil {
			// Deadline of read
			log.Println("Client may be disconnected")
			break
		}
	}
}
