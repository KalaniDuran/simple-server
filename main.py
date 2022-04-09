from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os

hostName = 'localhost'
serverPort = 8080

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        match self.path:
            case "/ping":
                self.ping()
            case "/skeleton":
                self.skeleton()
            case _:
                self.default()
            

    def ping(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("pong", "utf-8"))
    
    def default(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Request: %s" % self.path, "utf-8"))

    def skeleton(self):
        self.send_response(200)
        self.send_header("Content-type", "image/gif")
        self.end_headers()
        self.wfile.write(MyHandler.load(os.getcwd() + "/images/skelly.gif"))
    
    def load(file):
        with open(file, 'rb') as file_handle:
            return file_handle.read()
        # skelly

if __name__ == '__main__':
    webServer = HTTPServer((hostName, serverPort), MyHandler)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try: 
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")