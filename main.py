from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import json
import cgi
import sqlite3

hostName = 'localhost'
serverPort = 8080
connection = sqlite3.connect("/Users/Kalani/test.db")
connection.row_factory = sqlite3.Row

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        match self.path:
            case "/createuser":
                pass
            case "/createbook":
                pass
            case "/assignbook":
                pass
            case _:
                self.default()
        
        """ ctype, _ = cgi.parse_header(self.headers.get('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(message).encode('utf-8')) """

    def do_GET(self):
        match self.path:
            case "/ping":
                self.ping()
            case "/skeleton":
                self.skeleton()
            case "/getuser":
                self.getUser() 
            case "/getbook":
                pass
            case "/getbooksread":
                pass
            case _:
                self.default()

    def getUser(self):
        ctype, _ = cgi.parse_header(self.headers.get('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        #print(type(message))
        #print(dict(message))

        result = connection.execute("""
            SELECT reader_id, name
            FROM readers 
            WHERE reader_id=:reader_id
            AND name=:name""", message).fetchall()

        print(type(result))

        for row in result:
            print(dict(row))

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        for row in result:
            self.wfile.write(json.dumps(dict(row)).encode('utf-8'))

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