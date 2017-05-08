# coding=utf-8
"""Connections"""
import logging
from typing import NamedTuple, List
from urllib.parse import urlparse, ParseResult

import psycopg2
import psycopg2.extras

from config import DATABASE_URL

log = logging.getLogger(__name__)


class DatabaseAdapter:
    """More friendly adapter for the database, takes care of logging and abstracts the connection/cursor"""

    def __init__(self, url: str = DATABASE_URL):
        connection_data: ParseResult = urlparse(url)
        self.username: str = connection_data.username
        self.password: str = connection_data.password
        self.database: str = connection_data.path[1:]
        self.hostname: str = connection_data.hostname

    def __str__(self):
        return 'Database adapter'

    def __repr__(self):
        return f'DatabaseAdapter(username={self.username}, hostname={self.hostname}, database={self.database})'

    @property
    def connection(self) -> psycopg2.extensions.connection:
        """Creates and returns new connection to the database"""
        conn: psycopg2.extensions.connection = psycopg2.connect(
            database=self.database,
            user=self.username,
            password=self.password,
            host=self.hostname,
            connection_factory=psycopg2.extras.NamedTupleConnection,
            cursor_factory=psycopg2.extras.NamedTupleCursor
        )
        conn.autocommit = True
        log.debug("Connection made to host: %s, database: %s. Server version: %s, server encoding: %s",
                  self.hostname, self.database, conn.server_version, conn.encoding)
        return conn

    @property
    def cursor(self) -> psycopg2.extras.NamedTupleCursor:
        """Creates and returns new database cursor"""
        with self.connection as conn:
            return conn.cursor()

    def select(self, query: str, *args) -> NamedTuple:
        """Wrapped execute around select statement for single result"""
        with self.cursor as cur:
            cur.execute(query, args)
            result = cur.fetchone()
            log.debug("Ran select query\n'%s'\nResult: %s", _query_for_log(cur.query), result)
        return result

    def select_all(self, query: str, *args) -> List[NamedTuple]:
        """Wrapped execute around select statement for multiple results"""
        with self.cursor as cur:
            cur.execute(query, args)
            result = cur.fetchall()
            log.debug("Ran select all query\n'%s'\nResult: %s", _query_for_log(cur.query), result)
        return result

    def delete(self, query: str, *args) -> int:
        """Wrapped execute around delete statement"""
        with self.cursor as cur:
            cur.execute(query, args)
            log.debug("Ran delete query\n'%s'\nRows affected: %s", _query_for_log(cur.query), cur.rowcount)
            row_count = cur.rowcount
        return row_count

    def insert(self, query: str, *args):
        """Wrapped execute around insert statement"""
        with self.cursor as cur:
            cur.execute(query, args)
            log.debug("Ran insert query\n'%s'", _query_for_log(cur.query))

    def update(self, query: str, *args) -> int:
        """Wrapped execute around update statement"""
        with self.cursor as cur:
            cur.execute(query, args)
            log.debug("Ran update query\n'%s'\nRows affected: %s", _query_for_log(cur.query), cur.rowcount)
            row_count = cur.rowcount
        return row_count


def _query_for_log(query: bytes) -> str:
    """
    Takes a query that ran returned by psycopg2 and converts it into nicely loggable format
    with no newlines, extra spaces, and converted to string
    
    :param query:   Query ran by psycopg2
    :return:        Claned up string representing the query
    """
    return ' '.join(query.decode().replace('\n', ' ').split())

db: DatabaseAdapter = DatabaseAdapter()
