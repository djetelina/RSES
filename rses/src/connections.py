# coding=utf-8
import psycopg2
from urllib.parse import urlparse, ParseResult

from config import DATABASE_URL

class DatabaseAdapter:
    def __init__(self, url: str=DATABASE_URL):
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
        self.connection.autocommit=True


db: DatabaseAdapter = DatabaseAdapter()
