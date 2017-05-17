# coding=utf-8
"""Flask app, just imports the otherwise modular blueprints and takes care of basic auth"""
from functools import wraps

from flask import Flask, session, request, abort, url_for, redirect, render_template, flash

from blueprints.api.api import rses_api_bp

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(rses_api_bp)


def public(endpoint):
    """A decorator for endpoints that flags them as publicly accessible"""
    @wraps(endpoint)
    def public_endpoint(*args, **kwargs):
        return endpoint(*args, **kwargs)
    public_endpoint._is_public = True
    return public_endpoint


@app.before_request
def before_request():
    """Make sure no-one without master password enters"""
    if getattr(app.view_functions.get(request.endpoint, False), '_is_public', False):
        return
    if '/static/' in request.path:
        return
    if not session.get('authorized', False):
        return redirect(url_for('authorize'))


@app.route('/authorize', methods=['GET', 'POST'])
@public
def authorize():
    """Very basic authorization"""
    if request.method == 'POST':
        password: str = request.form.get('password')
        if password == app.config['RSES_MASTER_PASSWORD']:
            session['authorized'] = True
            return redirect('/')
        else:
            flash("Invalid password")

    return render_template('authorize.html')


# Registering stuff based on if web client is wanted
if app.config['RSES_WEB_CLIENT']:
    from blueprints.client.client import rses_web_client_bp
    app.register_blueprint(rses_web_client_bp)
else:
    # Redirect root url to API index if not running web client
    if not app.config['RSES_WEB_CLIENT']:
        def home():
            return redirect(url_for('RSES_API.index'))
        app.route('/')(home)

if __name__ == '__main__':
    port = app.config['PORT']
    app.run(host='0.0.0.0', port=port, debug=True)
