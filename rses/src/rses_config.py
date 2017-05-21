# coding=utf-8
"""Configuration"""
import os

SECRET_KEY: str = os.environ.get('SECRET_KEY', 'SUPER_SECRET')
PORT: int = int(os.environ.get('PORT', 5000))
DATABASE_URL: str = os.environ.get('RSES_DB_URL') or os.environ.get('DATABASE_URL')
# Do you want a flask client
RSES_WEB_CLIENT: bool = True
