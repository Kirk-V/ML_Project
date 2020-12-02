#!/usr/bin/python3
import http.server
import socketserver
import json
import base64
import mimetypes

#https://blog.anvileight.com/posts/simple-python-http-server/#do-post
class Handler(http.server.SimpleHTTPRequestHandler):
    count = 0
    
    def do_GET(self):        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        if self.path == "/post/send_request":
            print("got request")

            #look at header
            content_length = int(self.headers["Content-Length"])
            file_type = self.headers["Content-type"]
            if file_type != "application/json":
                self.send_response(400)
                self.end_headers()
                response = json.dumps(["error", "not json data"])
                self.wfile.write(response.encode())
                print("sent 400 repsonse")
                return

            self.send_response(200)
            self.end_headers()

            #unpack data
            body = self.rfile.read(content_length)
            data = json.loads(body)
            
            start = float(data["start"])
            end = float(data["end"])
            file_ext = mimetypes.guess_extension(data["file_type"])
            media_file = base64.b64decode(data["media_file"])
            
            f = open("./tmp/" + str(Handler.count) + file_ext, "wb")
            Handler.count += 1
            f.write(media_file);
            f.close();
            
            #call inference function, return images, names, probabilities
            #put into response format with JSON or XML
            
            response = json.dumps(["hello world"])
            
            self.wfile.write(response.encode())
            print("sent 200 repsonse")
            
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
