#!/usr/bin/env python3
# coding=utf-8
"""Run - mainly for development"""

from flask_app.app import app

port = app.config['PORT']
app.run(host='0.0.0.0', port=port, debug=True)
