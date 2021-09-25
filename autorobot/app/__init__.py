# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 11:22:18 2021

@author: alspe
"""

from flask import Flask

from .config import Config



# Initialisation et configuration de la session
app = Flask(__name__)
app.config.from_object(Config)


# Initialisation des chemins html
from autorobot.app import views