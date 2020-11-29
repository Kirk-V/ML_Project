#!/usr/bin/python3
import http.server
import socketserver

class Handler(http.server.SimpleHTTPRequestHandler):    
    def do_GET(self):
        if self.path == "/get/get_result":
            print("result")
            #get result
            return
        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
            
    def do_POST(self):
        if self.path == "/post/send_request":
            print("request")
            #get file
            
    
            
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
