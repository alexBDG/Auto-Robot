# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 11:31:14 2021

@author: alspe
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        b'\xc2\xdc^*\xf1w\xce\xb7\xdd\xb7f\xf2V\xb1v\x03'
