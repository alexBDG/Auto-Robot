# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 14:31:56 2021

@author: alspe
"""

import io
import cv2
import logging
import traceback
import socketserver
import threading
from http import server

PAGE="""\
<html>
<head>
<title>OpenCV MJPEG streaming demo</title>
</head>
<body>
<h1>MJPEG Streaming</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

class Streaming(threading.Thread):
    def __init__(self):
        self.frame = None
        self.cap = cv2.VideoCapture(0)
        super().__init__()

    def run(self):
        while True:
            ret, img = self.cap.read()
            if not ret:
                print('[ERROR] no image from camera')
                quit()
            ret, jpg = cv2.imencode('.jpg', img)
            self.frame = jpg.tobytes()

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    frame = stream.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
    
    def handel(self):
        self.server._shutdown_request = True
        print('[INFO] shutdown requested')
        



if __name__ == "__main__":
    
    stream = Streaming()
    stream.start()
    
    address = ('', 9000)
    with StreamingServer(address, StreamingHandler) as server:
        server.serve_forever()
    
    print('[INFO] End')
    
    
