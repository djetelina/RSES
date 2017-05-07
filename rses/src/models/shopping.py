# coding=utf-8
from typing import Union

import errors
from connections import db
from models.ingredient import Ingredient


class ShoppingItem(Ingredient):
    def __init__(self, name: str, amount: Union[float, None] = None):
        super().__init__(name)
        self._amount: Union[float, None] = amount

    @property
    def amount(self):
        if self._amount is None:
            return self.suggestion_threshold + 1
        return self._amount

    def create(self):
        if self._amount is None:
            errors.MissingParameter("amount")
        query = """
        INSERT INTO shopping_list (ingredient, wanted_amount)
        VALUES (%s, %s)
        """
        db.insert(query, self.name, self._amount)

    def __eq__(self, other):
        return self.name == other.name


class ShoppingList:
    def __init__(self):
        self.list = list()
        self.suggested_list = list()
        self.__add_from_db_list()
        self.__add_critical()
        self.__add_suggested()

    def __add_from_db_list(self):
        query = """
        SELECT ingredient, wanted_amount
        FROM shopping_list
        """
        res = db.select_all(query)
        for item in res:
            self.list.append(ShoppingItem(item['ingredient'], item['wanted_amount']))

    def __add_critical(self):
        query = """
        SELECT id
        FROM ingredient i
        LEFT JOIN stock s 
          ON i.id = s.ingredient
        WHERE count(s.amount_left) < i.rebuy_threshold
        """
        res = db.select_all(query)
        for item in res:
            item = ShoppingItem(item['id'])
            if item not in self.list:
                self.list.append(item)

    def __add_suggested(self):
        query = """
        SELECT id
        FROM ingredient i
        LEFT JOIN stock s 
          ON i.id = s.ingredient
        WHERE count(s.amount_left) < i.suggestion_threshold
        """
        res = db.select_all(query)
        for item in res:
            item = ShoppingItem(item['id'])
            if item not in self.list:
                self.suggested_list.append(item)
