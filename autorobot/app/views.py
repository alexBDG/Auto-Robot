# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 11:22:38 2021

@author: alspe
"""

import os
import time
import threading

from flask import render_template, request, jsonify

from autorobot.app import app
# from autorobot.server.server import VideoStreamingTest


EXPORTING_THREAD = None

# class ExportingThread(threading.Thread):
#     def __init__(self):
#         super().__init__()
#         self._stop_event = threading.Event()

#     def run(self):
#         # Lance le server
#         h, p = "localhost", 9000
#         self.stream = VideoStreamingTest(h, p)

#     def stop(self):
#         self.stream.stop_streaming()
#         while self.stream.state != "stopped":
#             time.sleep(0.5)
#         self._stop_event.set()

#     def stopped(self):
#         return self._stop_event.is_set()


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/stream/')
def stream():
    return render_template('stream.html')


@app.route('/start/', methods = ['POST'])
def start():
    print("[INFO] starting")
    return render_template('stream.html')

    # global EXPORTING_THREAD

    # # Launch script
    # EXPORTING_THREAD = ExportingThread()
    # EXPORTING_THREAD.start()

    # msg = 'Listening...'
    # return jsonify(msg)


# @app.route('/stream/', methods = ['POST'])
# def stream():

#     global EXPORTING_THREAD

#     # Get image
#     EXPORTING_THREAD.start()

#     if EXPORTING_THREAD.state
#     msg = 'Listening...'
#     return jsonify(msg)


@app.route('/stop/', methods = ['POST'])
def stop():
    pass
#     global EXPORTING_THREAD

#     # Stop script
#     EXPORTING_THREAD.stop()

#     msg = 'Stopped!'
#     return jsonify(msg)


# Gérer les erreurs
@app.errorhandler(404)
def err404(e):
    return render_template('404.html', err=e), 404


@app.errorhandler(500)
def not_found(e):
    return render_template('500.html', err=e), 500
