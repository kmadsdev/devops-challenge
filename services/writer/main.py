import http.server
import socketserver
# import json
import redis


class RequestHandler(http.server.BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')


    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()


    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self._send_cors_headers()
        self.end_headers()

        if self.path == '/health':
            self.wfile.write(b"up")


    def do_POST(self):
        if self.path != '/write':
            self.send_response(404)
            self._send_cors_headers()
            self.end_headers()
            return

        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode("utf-8")

            redisclient = redis.Redis(host="redis", port=6379)
            redisclient.set("SHAREDKEY", post_data)

            self.send_response(201)
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(b"written")

        except Exception as e:
            self.send_response(500)
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(str(e).encode("utf-8"))
            print("ERROR WRITING TO REDIS:", e)


handler_object = RequestHandler
server = socketserver.TCPServer(("", 8083), handler_object)
server.serve_forever()
