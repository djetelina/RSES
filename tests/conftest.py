# coding=utf-8
import logging
from typing import List, Any, Optional

from pytest import fixture

logging.basicConfig(level=logging.DEBUG)

class DatabaseMocker:
    """Super smart mocker for the database"""
    def __init__(self, return_values: Optional[List[Any]]=None, rowcount: int=1):
        if return_values is None:
            return_values = list()
        self.return_values: List[Any] = return_values
        self.rowcount: int = rowcount
        self.cursor = self
        self.query = None
        self.fetchall = self.fetchone

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __call__(self, *args, **kwargs):
        return self

    def execute(self, query, args):
        self.query = (query % args).encode()
        pass

    def fetchone(self):
        return self.return_values.pop(0)


@fixture(scope='function')
def database():
    return DatabaseMocker
