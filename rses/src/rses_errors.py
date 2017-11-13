# coding=utf-8
"""Errors"""
from typing import Optional, Type


class DoesNotExist(Exception):
    """When something does not exist"""

    def __init__(self, what: Type[object], identifier: str = '-', add_info: Optional[str] = None) -> None:
        """
        :param what:            The wanted object (uninitiated)
        :param identifier:      The identifier (primary key) for the object
        :param add_info:        Additional info
        """
        # We care about the name of the class itself
        self.what: str = what.__name__
        self.identifier: str = identifier
        self.add_info: Optional[str] = add_info

    def __str__(self):
        message = f'{self.what} identified by {self.identifier} does not exist. '
        if self.add_info is not None:
            message += self.add_info
        return message


class AlreadyExists(Exception):
    """When something already exists"""

    def __init__(self, what: object, relation: Optional[object] = None) -> None:
        """
        :param what:        An instance of an object that already exists
        :param relation:    If the object exists in relation to something else
        """
        self.what: object = what
        self.relation: Optional[object] = relation

    def __str__(self):
        if self.relation is not None:
            return f'{repr(self.what)} in relation to {repr(self.relation)} already exists'
        return f'{repr(self.what)} already exists'


class MissingParameter(Exception):
    """When required parameter is missing for specific action"""
    def __init__(self, parameter: str) -> None:
        """
        :param parameter:   Name of the parameter that is missing
        """
        self.parameter = parameter

    def __str__(self):
        return f'Missing parameter {self.parameter}'


class NotEnoughIngredients(Exception):
    """Error raised when ingredients are missing to cook a recipe"""
    pass
