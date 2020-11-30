#!/usr/bin/python3
import http.server
import socketserver
from io import BytesIO
import mimetypes

#https://blog.anvileight.com/posts/simple-python-http-server/#do-post
class Handler(http.server.SimpleHTTPRequestHandler):
    count = 0
    
    def do_GET(self):        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        if self.path == "/post/send_request":
            print("got request")
            
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            file_type = self.headers["Content-type"]
            file_ext = mimetypes.guess_extension(file_type);
            self.send_response(200)
            self.end_headers()
            
            f = open("./tmp/" + str(Handler.count) + file_ext, "wb")
            Handler.count += 1
            f.write(body);
            f.close();
            
            #call inference function, return images, names, probabilities
            #put into response format with JSON or XML
            
            response = BytesIO()
            response.write(b"This is a POST response.")
            self.wfile.write(response.getvalue())
            print("sent repsonse")
            
def main():
    host = "127.0.0.1"
    port = 8080

    httpd = socketserver.TCPServer((host, port), Handler)
    print("Server started at " + host + ":" + str(port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Closing the server.")
        httpd.shutdown()
        httpd.server_close()
        raise


if __name__ == "__main__":
    main()
