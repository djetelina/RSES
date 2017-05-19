# coding=utf-8
"""Web client"""
import os
from functools import wraps

from flask import Blueprint, render_template, current_app, request, session, redirect, url_for, flash

rses_web_client_bp = Blueprint('RSES_CLIENT', __name__, url_prefix='/rses',
                               template_folder='templates', static_folder='static',
                               static_url_path='/static/web_client')


@rses_web_client_bp.context_processor
def inject_menu_items() -> dict:
    return dict(menu_items=[
        {
            'title': '<i class="fa fa-home" aria-hidden="true"></i> Home',
            'url': '/',
            'function_name': 'home',
            'children': None
        },
        {
            'title': '<i class="fa fa-wrench" aria-hidden="true"></i> Manage',
            'children': [{
                'title': '<i class="fa fa-folder-open-o" aria-hidden="true"></i> Ingredient types',
                'function_name': 'ingredient_types'
            }]
        }
    ])


def public(endpoint):
    """A decorator for endpoints that flags them as publicly accessible"""

    @wraps(endpoint)
    def public_endpoint(*args, **kwargs):
        return endpoint(*args, **kwargs)

    public_endpoint._is_public = True
    return public_endpoint


@rses_web_client_bp.before_request
def before_request():
    """Make sure no-one without master password enters"""
    if getattr(current_app.view_functions.get(request.endpoint, False), '_is_public', False):
        return
    if '/static/' in request.path:
        return
    if not session.get('authorized', False):
        return redirect(url_for('RSES_CLIENT.authorize'))


@rses_web_client_bp.route('/authorize', methods=['GET', 'POST'])
@public
def authorize():
    """Very basic authorization"""
    if request.method == 'POST':
        password: str = request.form.get('password')
        if password == os.environ.get('RSES_MASTER_PASSWORD', 'kitchen'):
            session['authorized'] = True
            return redirect('/')
        else:
            flash("Invalid password")

    return render_template('rses_authorize.html')


@rses_web_client_bp.route('/')
def home():
    return render_template('rses_home.html')


@rses_web_client_bp.route('/manage/ingredient_types')
def ingredient_types():
    return render_template('stock/ingredient_types.html')
