#!/usr/bin/python3.7
import sys
import os

import http.server
import socketserver
import json
import mimetypes

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import *

sys.path.append("../src")
from detect_classify import *

#https://blog.anvileight.com/posts/simple-python-http-server/#do-post
class Handler(http.server.SimpleHTTPRequestHandler):
    count = 0
    
    def do_GET(self):
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        if self.path == "/post/send_json":
            print("got send_json request")

            #look at header
            content_length = int(self.headers["Content-Length"])
            file_type = self.headers["Content-Type"]
            
            if file_type != "application/json":
                self.send_header("Content-Type", "application/json")
                self.send_response(400)
                self.end_headers()
                
                response = json.dumps(["status", "error: not json data"])
                self.wfile.write(response.encode())
                print("send_json sent 400 repsonse")
                return
            
            #unpack data
            body = self.rfile.read(content_length)
            data = json.loads(body)
            
            start = float(data["start"])
            end = float(data["end"])
            file_type = data["file_type"]
            
            f = open("./tmp/" + str(Handler.count) + ".txt", "w")
            f.write(str(Handler.count) + "\n" + str(start) + "\n" + str(end) + "\n" + file_type + "\n");
            f.close();

            response = json.dumps({"json": "recieved"})
    
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            self.wfile.write(response.encode())
            print("send_json sent 200 repsonse")
            
        if self.path == "/post/send_data":
            print("got send_data")

            #look at header
            content_length = int(self.headers["Content-Length"])
            file_type = self.headers["Content-Type"]
            file_ext = mimetypes.guess_extension(file_type);

            #unpack data
            body = self.rfile.read(content_length)
            #save video file
            f = open("./tmp/" + str(Handler.count) + file_ext, "wb")
            f.write(body);
            f.close();

            #read in metadata
            f = open("./tmp/" + str(Handler.count) + ".txt", "r")
            lines = f.readlines();
            f.close()
            
            start_time = float(lines[1])
            end_time = float(lines[2])

            ffmpeg_extract_subclip("./tmp/" + str(Handler.count) + file_ext,
                                   start_time, end_time,
                                   "./tmp/" + str(Handler.count) + "_clip" + file_ext)

            os.chdir("../src")
            print(os.getcwd())
            classes = videoToFaces("../website/tmp/" + str(Handler.count) + "_clip" + file_ext,
                                   "../website/tmp/" + str(Handler.count) + "_clip_annotated.mp4")
            print(os.getcwd())
            os.chdir("../website")
                        
            response = json.dumps({"results": [{"class": "Actor 1", "probability": "0.80", "color": "blue"},
                                               {"class": "Actor 2", "probability": "0.10", "color": "Red"},
                                               {"class": "Actor 3", "probability": "0.10", "color": "Green"}]})
            
            self.send_response(200)
            self.send_header("Content-Type", "video/mp4")
            self.end_headers()
            
            self.wfile.write(response.encode())
            print("send_data sent 200 repsonse")            
            
        if self.path == "/post/get_data":
            print("got get_data request")

            #should change to proper clip with boxes
            f = open("./tmp/" + str(Handler.count) + "_clip_annotated.mp4", "rb")
            annotated_clip = f.read()
            f.close()

            self.send_response(200)
            self.send_header("Content-Type", "video/mp4")
            self.end_headers()

            self.wfile.write(annotated_clip)
            print("get_data sent 200 repsonse")
                        
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
