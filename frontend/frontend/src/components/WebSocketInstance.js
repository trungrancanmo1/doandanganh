
class WebSocketInstance {
  static instance = null
    constructor() {
      if (WebSocketInstance.instance === null){
        console.log("hereeeeeeeeee")
        this.socket = null;
        this.token = null;
        this.listeners = [];
        this.connected = false;
        WebSocketInstance.instance = this
      }
      return WebSocketInstance.instance
    }

    // Kết nối WebSocket nếu chưa kết nối
    connect(token) {
        if (this.connected) {
            return; // Nếu đã kết nối, không làm gì cả
        }

        if (!token) {
            throw new Error('Token is required to establish a WebSocket connection.');
        }

        this.token = token;
        this.socket = new WebSocket(`ws://localhost:8080/ws?token=${this.token}`);
        this.connected = true;

        this.socket.onopen = () => {
            console.log("WebSocket connected");
            this.connected = true;
            this.notifyListeners('connected');
        };

        this.socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this.notifyListeners('message', data);
            } catch (error) {
                console.error('WebSocket message error:', error);
            }
        };

        this.socket.onerror = (error) => {
            console.error("WebSocket error:", error);
            this.notifyListeners('error', error);
        };

        this.socket.onclose = () => {
            console.log("WebSocket closed");
            this.connected = false;
            this.notifyListeners('disconnected');
        };
    }

    // Gửi tin nhắn đến WebSocket
    sendMessage(message) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(message);
        } else {
            console.error('Cannot send message, WebSocket is not open');
        }
    }

    // Đóng kết nối WebSocket
    disconnect() {
        console.log("đóng socket")
        if (this.socket) {
            this.socket.close();
            this.socket = null;
            this.connected = false;
            this.instance = null
        }
    }

    // Thêm listener cho các sự kiện WebSocket
    addListener(event, callback) {
        this.listeners.push({ event, callback });
    }

    // Xóa listener cho WebSocket
    removeListener(event, callback) {
        this.listeners = this.listeners.filter(
            (listener) => !(listener.event === event && listener.callback === callback)
        );
    }

    // Thông báo tất cả listeners về sự kiện
    notifyListeners(event, data) {
        this.listeners.forEach(listener => {
            if (listener.event === event) {
                listener.callback(data);
            }
        });
    }

    // Kiểm tra trạng thái kết nối
    isConnected() {
        return this.connected;
    }

    print(){
        console.log(this.socket)
        console.log(this.token)
        console.log(this.listeners)
        console.log(this.connected)
    }
}

// Tạo instance của WebSocketInstance và export để sử dụng ở các nơi khác
const wsInstance = new WebSocketInstance()
//Object.freeze(wsInstance)
export default wsInstance;
