# coding=utf-8
"""Connections"""
from urllib.parse import urlparse, ParseResult

import psycopg2

from config import DATABASE_URL


class DatabaseAdapter:
    """More friendly adapter for the database, takes care of logging and abstracts the connection/cursor"""

    def __init__(self, url: str = DATABASE_URL):
        connection_data: ParseResult = urlparse(url)
        username: str = connection_data.username
        password: str = connection_data.password
        database: str = connection_data.path[1:]
        hostname: str = connection_data.hostname
        self.connection: object = psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=hostname
        )
        self.connection.autocommit = True


db: DatabaseAdapter = DatabaseAdapter()
