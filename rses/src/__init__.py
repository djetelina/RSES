# coding=utf-8
"""The python source"""
import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from flask_app.blueprints.api.api import rses_api_bp
from flask_app.blueprints.client.client import rses_web_client_bp