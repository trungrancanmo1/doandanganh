# server.py
import http.server
import socketserver
import cgi
import os

HOST = "localhost"
PORT = 8000

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/upload_image":
            ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
            if ctype == 'multipart/form-data':
                postvars = cgi.parse_multipart(self.rfile, pdict)
                image_file = postvars.get('image')
                timestamp = postvars.get('timestamp', [b''])[0].decode('utf-8')
                location = postvars.get('location', [b''])[0].decode('utf-8')

                if image_file:
                    image_data = image_file[0].file.read()
                    filename = image_file[0].filename
                    filepath = os.path.join(UPLOAD_DIR, filename)
                    try:
                        with open(filepath, 'wb') as f:
                            f.write(image_data)
                        self.send_response(200)
                        self.send_header("Content-type", "text/plain")
                        self.end_headers()
                        self.wfile.write(f"Image '{filename}' uploaded successfully!".encode('utf-8'))
                        print(f"Image '{filename}' saved at {filepath}")
                        if timestamp:
                            print(f"Timestamp: {timestamp}")
                        if location:
                            print(f"Location: {location}")
                    except Exception as e:
                        self.send_response(500)
                        self.send_header("Content-type", "text/plain")
                        self.end_headers()
                        self.wfile.write(f"Error saving image: {e}".encode('utf-8'))
                else:
                    self.send_response(400)
                    self.send_header("Content-type", "text/plain")
                    self.end_headers()
                    self.wfile.write(b"No image file received")
                return

        # Handle other POST requests (like /data) as before
        elif self.path == "/data":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            print(f"Received POST data: {post_data}")
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Data received successfully!")
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found")

with socketserver.TCPServer((HOST, PORT), MyHandler) as httpd:
    print(f"Serving at http://{HOST}:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")