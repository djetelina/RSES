# coding=utf-8
"""Web client"""
from flask import Blueprint, render_template
rses_web_client_bp = Blueprint('RSES_CLIENT', __name__,
                               template_folder='client', static_folder='static',
                               static_url_path='/static/web_client')


@rses_web_client_bp.context_processor
def inject_menu_items() -> dict:
    return dict(menu_items=[
        {
            'title': 'Home',
            'url': '/',
            'function_name': 'home',
            'children': None
        },
        {
            'title': 'Manage',
            'children': [{
                'title': 'Ingredient types',
                'function_name': 'ingredient_types'
            }]
        }
    ])


@rses_web_client_bp.route('/')
def home():
    return render_template('client/home.html')


@rses_web_client_bp.route('/manage/ingredient_types')
def ingredient_types():
    return render_template('client/stock/ingredient_types.html')
