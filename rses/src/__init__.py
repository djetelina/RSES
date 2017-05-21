# coding=utf-8
"""The python source, importable if someone adds RSES as a submodule"""
import sys
import os

# So that our code's imports works in different application - careful about namespaces!
# Top level should be  prefixed with `rses_`
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# Expose the blueprints
from flask_app.blueprints.api.api import rses_api_bp
from flask_app.blueprints.client.client import rses_web_client_bp
