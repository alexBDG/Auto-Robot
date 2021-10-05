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
import logging
import argparse
import traceback
import socketserver
import threading
from http import server

try:
    from ..hardware.motor import RobotMotors, IS_GPIO_AVAILABLE
except ImportError:
    sys.path.insert(0, os.path.join('..', '..'))
    from autorobot.hardware.motor import RobotMotors, IS_GPIO_AVAILABLE

import socket



class StreamingServer(object):
    
    def __init__(self, host, port, verbose=0):
        self.host = host
        self.port = port
        self.verbose = verbose
    
    def serve_forever(self):
        # Start the connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if self.verbose>0:
                print("[CMD] starting connection...")    
            s.bind((self.host, self.port))
            if self.verbose>0:
                print("[CMD] listening...")    
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                if self.verbose>0:
                    print("[CMD] connection", addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        if self.verbose>0:
                            print("[CMD] no data - stopped")
                        break
                    # Decode and transfoms to list
                    data = data.decode().split('\r\n')
                    if self.verbose>0:
                        print("[CMD] data received", data)
                        print("[CMD] data received", json.loads(data[-1]))
                        
                    # Send response
                    response_proto = 'HTTP/1.1'
                    response_status = '200'
                    response_status_text = 'OK' # this can be random
                    response_content = {
                        'Access-Control-Allow-Origin': '*'
                    }
        
                    # sending all this stuff
                    response = '{} {} {}\r\n'.format(
                        response_proto, response_status, response_status_text
                    )
                    for k, v in response_content.items():
                        response += '{}: {}\r\n'.format(k, v)
                    conn.sendall(response.encode())





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
    
    
    server = StreamingServer('', 9500, args['verbose'])
    server.serve_forever()
    
    print('[INFO] End')
    
    
