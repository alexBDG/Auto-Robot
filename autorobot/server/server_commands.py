# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 21:12:27 2021

@author: alspe
"""

import os
import io
import sys
import cv2
import time
import json
import socket
import logging
import argparse
import traceback
import socketserver
import threading
from http import server

try:
    from ..hardware.motor import RobotMotors, IS_GPIO_AVAILABLE
except:
    sys.path.insert(0, os.path.join('..', '..'))
    from autorobot.hardware.motor import RobotMotors, IS_GPIO_AVAILABLE


class StreamingHandler(server.BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == '/':
            try:
                content = self.rfile.read(int(self.headers['Content-Length']))
                content = json.loads(content.decode())
                print('content', content)
                # Read
                v = content['vector']
                speed = content['speedVelocity']
                rotation_speed = content['speedRotation']
                if rm is not None:
                    rm.move(-v[1]*speed, -v[0]*rotation_speed)
                is_valid = True

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                is_valid = False

            finally:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"is_valid": is_valid}).encode())
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

    parser = argparse.ArgumentParser(prog='Server-Command')
    parser.add_argument(
        '-v', '--verbose',
        type=float, default=0,
        help='Display informations if non null.'
    )
    args = vars(parser.parse_args())

    if IS_GPIO_AVAILABLE:
        rm = RobotMotors(
            21, 20, 16, # Left motor
            18, 23, 24, # Right motor
            verbose = args['verbose']
        )
    else:
        rm = None

    address = ('', 9500)
    with StreamingServer(address, StreamingHandler) as server:
        server.serve_forever()

    print('[INFO] End')
