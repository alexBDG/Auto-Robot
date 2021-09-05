# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 12:05:46 2021

@author: alspe
"""

import time
import pygame
import cv2
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGroupBox
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QPainter

from game import Game

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (-1000,-1000)


#======#
# GAME #
#======#

class GameThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, resolution, parent=None):
        super(GameThread, self).__init__(parent)
        self.resolution = resolution

    def run(self):
        pygame.init()
        self.g = Game(self.resolution, 30, stand_alone=False)
        
        # <start> loop
        pygame.init()
        self.g.screen = pygame.display.set_mode(self.g.res)
        
        # <run> loop
        while self.g.is_running:
            for evt in pygame.event.get():
                self.g.manage_events(evt)
            v = self.g.manage_pressed_keys()
            self.g.update()
            #=================================================================#
            # Update the application
            w = self.g.screen.get_width()
            h = self.g.screen.get_height()
            data = self.g.screen.get_buffer().raw
            image = QImage(data, w, h, QImage.Format_RGB32)
            image = image.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(image)
            #=================================================================#
        self.g.quit()



class GameApp(QWidget):

    def __init__(self, parent=None):
        super(GameApp, self).__init__(parent)
        self.title = "Game"
        self.resolution = (640, 480)
        self.initUI()


    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))


    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(30+self.resolution[0], 30+self.resolution[1])

        # Create the game widget
        self.label = QLabel(self)
        self.label.resize(20+self.resolution[0], 20+self.resolution[1])
        self.label.move(10, 10)
        
        # Create the game
        gth = GameThread(self.resolution, self)
        gth.changePixmap.connect(self.setImage)
        gth.start()
        # Wait in order to works
        time.sleep(1)



#========#
# CAMERA #
#========#

class VideoThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)



class CameraApp(QWidget):

    def __init__(self, parent=None):
        super(CameraApp, self).__init__(parent)
        self.title = "Camera"
        self.resolution = (640, 480)
        self.initUI()


    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))


    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(30+self.resolution[0], 30+self.resolution[1])
        
        # Create a label
        self.label = QLabel(self)
        self.label.resize(20+self.resolution[0], 20+self.resolution[1])
        self.label.move(10, 10)
        
        # Create the stream
        vth = VideoThread(self)
        vth.changePixmap.connect(self.setImage)
        vth.start()



#==============#
# MAIN WINDOWS #
#==============#

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.title = "Main Windows"
        self.resolution = (60+2*640, 60+480)
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.resolution[0], self.resolution[1])

        hlayout = QHBoxLayout()
        vlayout = QVBoxLayout()

        cameraWidget = CameraApp()
        hlayout.addWidget(cameraWidget)

        gameWidget = GameApp()
        hlayout.addWidget(gameWidget)

        hGroupBox = QGroupBox()
        hGroupBox.setLayout(hlayout)
        
        vlayout.addWidget(hGroupBox)
        
        widget = QWidget()
        widget.setLayout(vlayout)
        widget.resize(self.resolution[0], self.resolution[1])
        self.setCentralWidget(widget)



#=======#
# TESTS #
#=======#

if __name__ == '__main__':
    app = QApplication([])
    
    window = MainWindow()
    app.exec()


