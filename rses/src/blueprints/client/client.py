# coding=utf-8
"""Web client"""
from flask import Blueprint, render_template
rses_web_client_bp = Blueprint('RSES_CLIENT', __name__,
                               template_folder='client', static_folder='static',
                               static_url_path='/static/web_client')

@rses_web_client_bp.route('/')
def home():
    return render_template('client/home.html')