#!/usr/bin/env python3
# coding=utf-8

from flask_app.app import app

port = app.config['PORT']
app.run(host='0.0.0.0', port=port, debug=True)
