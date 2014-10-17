import time
import BaseHTTPServer
from random import randint


from webcam import WebcamFeed

HOST_NAME = 'localhost'  # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8080  # Maybe set this to 9000.


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    webcam_feed = None

    def _process_request(self):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()


    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write('Webcam alive?: {}'.format(self.webcam_feed.isAlive()))
        self.wfile.write('x={wc.xOut}, y={wc.yOut}'.format(wc=self.webcam_feed))


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    webcam_feed = WebcamFeed()
    webcam_feed.start()
    MyHandler.webcam_feed = webcam_feed
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except (Exception, KeyboardInterrupt) as exc:
        webcam_feed.join()
        httpd.server_close()
    finally:    
        print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
