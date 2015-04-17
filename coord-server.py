#!/usr/bin/env python
import json
import time
import BaseHTTPServer
from webcam import WebcamFeed

HOST_NAME = 'localhost'  # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8080  # Maybe set this to 9000.


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    webcam_feed = None

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        # self.wfile.write('Webcam alive?: {}'.format(self.webcam_feed.isAlive()))
        x, y = self.webcam_feed.get_rel_coords()
        self.wfile.write(json.dumps({'x': x,'y':y}))

if __name__ == '__main__':
    print("HELLO!")
    server_class = BaseHTTPServer.HTTPServer
    webcam_feed = WebcamFeed()
    webcam_feed.start()
    MyHandler.webcam_feed = webcam_feed
    MyHandler.curX = 0
    MyHandler.curY = 0
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except (Exception, KeyboardInterrupt) as exc:
        webcam_feed.join()
        httpd.server_close()
    finally:    
        print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
