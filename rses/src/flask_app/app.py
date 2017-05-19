# coding=utf-8
"""Flask app, just imports the otherwise modular blueprints and it's configuration"""
from flask import Flask, url_for, redirect

from flask_app.blueprints.api.api import rses_api_bp

app = Flask(__name__)
app.config.from_object('rses_config')
app.register_blueprint(rses_api_bp)

# Registering stuff based on if web client is wanted
if app.config['RSES_WEB_CLIENT']:
    from flask_app.blueprints.client.client import rses_web_client_bp

    app.register_blueprint(rses_web_client_bp)


    def home():
        return redirect(url_for('RSES_CLIENT.home'))


    app.route('/')(home)
else:
    # Redirect root url to API index if not running web client
    def home():
        return redirect(url_for('RSES_API.index'))


    app.route('/')(home)

if __name__ == '__main__':
    port = app.config['PORT']
    app.run(host='0.0.0.0', port=port, debug=True)
