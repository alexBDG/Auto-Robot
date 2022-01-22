# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 11:21:00 2021

@author: alspe
"""

import sys
sys.path.append("..")

from autorobot.app import app



if __name__ == '__main__':
    """Lancement de l'application flask.

    Exemples:
    ---------
    >>> !set FLASK_APP=site.py
    >>> !flask run -h '0.0.0.0' -p 8000 --cert=cert.pem --key=key.pem
    """

    app.run(
        debug=True,
        host="0.0.0.0",
        port=8000,
        threaded=True
    )