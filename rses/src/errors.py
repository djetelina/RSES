# coding=utf-8
from typing import Union

class DoesNotExist(Exception):
    def __init__(self, what: object, identifier: str='-', add_info: Union[None, str]=None):
        # We care about the name of the class itself
        self.what: str = what.__name__
        self.identifier: str = identifier
        self.add_info: Union[None, str] = add_info

    def __str__(self):
        message = f'Error: {self.what} identified by {self.identifier} does not exist. '
        if self.add_info is not None:
            message += self.add_info
        return message


class AlreadyExists(Exception):
    def __init__(self, what: object):
        self.what: object = what

    def __str__(self):
        return f'Error: {repr(self.what)} already exists'


class MissingParameter(Exception):
    def __init__(self, parameter: str):
        self.parameter = parameter

    def __str__(self):
        return f'Error: Missing parameter {self.parameter}'
