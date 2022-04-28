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
    """
    Handles all requests that want to create data within the database.
    All cases are based on the URL path of the request.
    """
    def do_POST(self):
        match self.path:
            case "/createuser":
                self.createUser()
            case "/createbook":
                self.createBook()
            case "/assignbook":
                self.assignBook()
            case _:
                self.default()

    """
    Handles all requests that want to retrieve data, mainly from within the database.
    All cases are based on the URL path of the request.
    """
    def do_GET(self):
        match self.path:
            case "/ping":
                self.ping()
            case "/skeleton":
                self.skeleton()
            case "/getuser":
                self.getUser() 
            case "/getbook":
                self.getBook()
            case "/getbooksread":
                pass
            case _:
                self.default()
    
    """
    Aceepts JSON input with new user information in order to create a user within the database.
    New user information is accepted in this format:
    {
        "name" : "First and last name"
    }
    """
    def createUser(self):
        ctype, _ = cgi.parse_header(self.headers.get('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        connection.execute("""
        INSERT into readers(name) 
        VALUES (:name)""", message)

        connection.commit()

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes("User created", "utf-8"))

    """
    Aceepts JSON input with new book information in order to create a book within the database.
    New book information is accepted in this format:
    {
        "title" : "Title of book",
        "author" : "First and last name",
        "description" : "Short description of book"
    }
    """
    def createBook(self):
        ctype, _ = cgi.parse_header(self.headers.get('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        connection.execute("""
        INSERT into books(title, author, description) 
        VALUES (:title, :author, :description)""", message)

        connection.commit()

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes("Book created", "utf-8"))
    
    """
    Aceepts JSON input user and book information to denote a book being read by said user.
    Information is accepted in this format:
    {
        "name" : "First and last name",
        "title" : "Title of book"
    }
    """
    def assignBook(self):
        ctype, _ = cgi.parse_header(self.headers.get('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        connection.execute("""
        INSERT INTO books_read
        SELECT reader_id, book_id
        FROM readers, books
        WHERE name=:name and title=:title""", message)

        connection.commit()

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes("Book assigned", "utf-8"))
    
    
    """
    Aceepts JSON input user information to retrieve full user info.
    Information is accepted in this format:
    {
        "name" : "First and last name"
    }
    """
    def getUser(self):
        ctype, _ = cgi.parse_header(self.headers.get('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        result = connection.execute("""
            SELECT reader_id, name
            FROM readers 
            WHERE name=:name""", message).fetchall()

        connection.commit()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        for row in result:
            self.wfile.write(json.dumps(dict(row)).encode('utf-8'))

    """
    Aceepts JSON input book information to retrieve full book info.
    Information is accepted in this format:
    {
        "title" : "Title of book"
    }
    """
    def getBook(self):
        ctype, _ = cgi.parse_header(self.headers.get('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        result = connection.execute("""
            SELECT *
            FROM books 
            WHERE title=:title""", message).fetchall()

        connection.commit()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        for row in result:
            self.wfile.write(json.dumps(dict(row)).encode('utf-8'))

    """
    Simple ping request to check if server is up and functional.
    Returns "pong"
    """
    def ping(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("pong", "utf-8"))
    
    """
    Default case for any URL paths that aren't specifically covered.
    Returns "Request: /URLpath"
    """
    def default(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Request: %s" % self.path, "utf-8"))

    """
    Test case for returning .gif format.
    """
    def skeleton(self):
        self.send_response(200)
        self.send_header("Content-type", "image/gif")
        self.end_headers()
        self.wfile.write(MyHandler.load(os.getcwd() + "/images/skelly.gif"))
    
    """
    Helper function for opening and reading an image file.
    """
    def load(file):
        with open(file, 'rb') as file_handle:
            return file_handle.read()

if __name__ == '__main__':
    webServer = HTTPServer((hostName, serverPort), MyHandler)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try: 
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")