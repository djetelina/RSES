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

    # TODO look into http://initd.org/psycopg/docs/sql.html for query composition

    def __init__(self, url: str = DATABASE_URL):
        connection_data: ParseResult = urlparse(url)
        self.username: str = connection_data.username
        self.password: str = connection_data.password
        self.database: str = connection_data.path[1:]
        self.hostname: str = connection_data.hostname

    @property
    def connection(self) -> psycopg2.extensions.connection:
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
        with self.connection as conn:
            return conn.cursor()

    def select(self, query, *args) -> NamedTuple:
        with self.cursor as cur:
            cur.execute(query, args)
            result = cur.fetchone()
            log.debug("Ran select query\n'%s'\nResult: %s",
                      ' '.join(cur.query.decode().replace('\n', ' ').split()), result)
        return result

    def select_all(self, query, *args) -> List[NamedTuple]:
        # TODO convert to iterator possibly?
        with self.cursor as cur:
            cur.execute(query, args)
            result = cur.fetchall()
            log.debug("Ran select all query\n'%s'\nResult: %s",
                      ' '.join(cur.query.decode().replace('\n', ' ').split()), result)
        return result

    def delete(self, query, *args) -> int:
        with self.cursor as cur:
            cur.execute(query, args)
            log.debug("Ran delete query\n's'\nRows affected: %s",
                      ' '.join(cur.query.decode().replace('\n', ' ').split()), cur.rowcount)
            row_count = cur.rowcount
        return row_count

    def insert(self, query, *args):
        pass

    def update(self, query, *args) -> int:
        pass


db: DatabaseAdapter = DatabaseAdapter()

if __name__ == '__main__':
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    db = DatabaseAdapter(url='postgres://postgres:postgres@localhost/rses')
    db.select('SELECT id FROM ingredient')
    db.select_all("""SELECT id
    FROM ingredient""")
