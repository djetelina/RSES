# coding=utf-8
"""Objects related to shopping"""
from datetime import datetime
from typing import Union

from connections import db
from models.stock import Ingredient


class ShoppingItem(Ingredient):
    """For displaying in shopping list"""
    def __init__(self, id: int, amount: Union[float, None] = None) -> None:
        super().__init__(ingredient_id=id)
        self._amount: Union[float, None] = amount
        self.current_price: Union[float, None] = None
        self.expiration_date: Union[datetime.date, None] = None

    @property
    def status(self) -> str:
        """Whether the item is in cart, or not"""
        query = """
        SELECT status
        FROM shopping_list
        WHERE ingredient = %s
        """
        res = db.select(query, self._id)
        return res.status

    @property
    def amount(self) -> float:
        """How many units of this ingredient should be bought"""
        if self._amount is None:
            return self._suggestion_threshold + 1.0
        return self._amount

    def __str__(self):
        return f'{self.amount}x {self._unit} {self._name}'

    def __repr__(self):
        return f'ShoppingItem(name:{self._name}, _amount:{self.amount}, current_price: {self.current_price}, ' \
               f'average_price:{self.average_price}, status:{self.status})'

    def create(self) -> None:
        """Adds the item into the database of things to buy"""
        if self._amount is None:
            self._amount = self.amount
        query = """
        INSERT INTO shopping_list (ingredient, wanted_amount)
        VALUES (%s, %s)
        """
        db.insert(query, self._id, self._amount)

    def to_cart(self) -> None:
        """Marks the item as in cart"""
        query = """
        UPDATE shopping_list
        SET status = 'cart'
        WHERE ingredient = %s
        """
        db.update(query, self._id)

    def from_cart(self) -> None:
        """Moves the item back from 'cart' to on-list"""
        query = """
        UPDATE shopping_list
        SET status = 'list'
        WHERE ingredient = %s
        """
        db.update(query, self._id)

    def purchase(self) -> None:
        """Adds the item to stock and deletes it from shopping list database"""
        query_insert = """
        INSERT INTO stock (ingredient, amount, amount_left, expiration_date, price)
        VALUES (%s, %s, %s, %s, %s)
        """
        db.insert(query_insert, self._id, self.amount, self.amount, self.expiration_date, self.current_price)
        query_delete = """
        DELETE FROM shopping_list
        WHERE ingredient = %s
        """
        db.delete(query_delete, self._id)

    def __eq__(self, other):
        return self._id == other._id and self._name == other._name


class ShoppingList:
    """Shopping list that fills itself and is ready for serving"""
    def __init__(self):
        self.list = list()
        self.suggested_list = list()
        self.__add_from_db_list()
        self.__add_critical()
        self.__add_suggested()

    def __str__(self):
        return f'Shopping list: {self.list}, suggestions: {self.suggested_list}'

    def __repr__(self):
        return f'ShoppingList(list:{repr(self.list)}, suggested_list:{repr(self.suggested_list)})'

    def __add_from_db_list(self) -> None:
        query = """
        SELECT ingredient, wanted_amount
        FROM shopping_list
        """
        res = db.select_all(query)
        for item in res:
            self.list.append(ShoppingItem(item.ingredient, item.wanted_amount))

    def __add_critical(self) -> None:
        """
        Adds items to the shopping list that are under the critical threshold to rebuy.
        
        If the threshold is 0, it means it shouldn't be rebought
        """
        query = """
        SELECT id
        FROM ingredient i
        LEFT JOIN stock s 
          ON i.id = s.ingredient
        WHERE count(s.amount_left) < i.rebuy_threshold
        AND i.rebuy_threshold > 0
        """
        res = db.select_all(query)
        for item in res:
            item = ShoppingItem(item.id)
            item.create()
            if item not in self.list:
                self.list.append(item)

    def __add_suggested(self) -> None:
        """
        Suggests items for purchase, but does not add them to things to buy - this has to be done manually
        """
        query = """
        SELECT id
        FROM ingredient i
        LEFT JOIN stock s 
          ON i.id = s.ingredient
        WHERE count(s.amount_left) < i.suggestion_threshold
        AND i.suggestion_threshold > 0
        """
        res = db.select_all(query)
        for item in res:
            item = ShoppingItem(item.id)
            if item not in self.list:
                self.suggested_list.append(item)
