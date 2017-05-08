# coding=utf-8
"""Objects related to ingredients and stock"""
from typing import Union, List

import errors
from connections import db


class IngredientType:
    """
    For shopping list organization and filtering
    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'IngredientType(name={self.name})'

    def exists(self) -> bool:
        """Whether the ingredient type exists"""
        query = """
        SELECT * 
        FROM ingredient_type
        WHERE id = %s
        """
        res = db.select(query, self.name)
        return bool(res)

    def create(self):
        """Creates an ingredient type"""
        if self.exists():
            raise errors.AlreadyExists(self)
        query = """
        INSERT INTO ingredient_type (id)
        VALUES (%s)
        """
        db.insert(query, self.name)

    def delete(self):
        """Deletes an ingredient type"""
        if not self.exists():
            raise errors.DoesNotExist(IngredientType, identifier=self.name)
        query = """
        DELETE FROM ingredient_type
        WHERE id = %s
        """
        db.delete(query, self.name)

    def items(self) -> List[Ingredient]:
        """All ingredients of this type"""
        query = """
        SELECT id as id
        FROM ingredient
        WHERE ingredient_type = %s
        """
        res = db.select_all(query, self.name)
        ingredients = list()
        for item in res:
            ingredients.append(Ingredient(item.id))
        return ingredients


class Ingredient:
    """An ingredient to buy and use in recipes"""
    def __init__(
            self,
            name: str,
            unit: object = None,
            ingredient_type: object = None,
            suggestion_threshold: object = 0.0,
            rebuy_threshold: object = 0.0,
            durability: object = None,
            new: object = False
    ):
        """
        :param name:                    The name of the ingredient, as will be display everywhere
        :param unit:                    The measurable unit of the ingredient, can be virtually anything
        :param ingredient_type:         The type if ingredient that the item belongs to
        :param suggestion_threshold:    When the shopping system will recommend you to maybe purchse
        :param rebuy_threshold:         When the shopping system tells you to absolutely buy it next time you see it
        :param durability:              If specified, calculates the expiration date based on the date of purchase
        :param new:                     If this is an ingredient to be created, 
                                        so it doesn't try and load it from the database
        """
        self.name: str = name
        self.unit: Union[str, None] = unit
        self.type: IngredientType = ingredient_type
        self.suggestion_threshold: float = suggestion_threshold
        self.rebuy_threshold: float = rebuy_threshold
        self.durability: int = durability
        if not new:
            self.__load_from_db()

    @property
    def average_price(self) -> float:
        """Average price of the ingredient"""
        query = """
        SELECT avg(price) as average
        FROM stock
        WHERE ingredient = %s 
        ORDER BY time_bought DESC 
        LIMIT 30
        """
        return db.select(query, self.name).average

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Ingredient(name={self.name}, unit={self.unit}, type={self.type}, ' \
               f'suggestion_threshold={self.suggestion_threshold}, rebuy_threshold={self.rebuy_threshold}'

    def exists(self) -> bool:
        """
        :return:    If the ingredient exists
        """
        query = """
        SELECT * 
        FROM ingredient
        WHERE id = %s
        """
        res = db.select(query, self.name)
        return bool(res)

    def create(self):
        """
        Creates the ingredient, requires to have type and unit specified.
        
        Default thresholds are 0 and no durability is set.
        """
        required_params = dict(type=self.type, unit=self.unit)
        for name, param in required_params:
            if param is None:
                errors.MissingParameter(name)
        if not IngredientType(self.type).exists():
            IngredientType(self.type).create()
        if self.exists():
            raise errors.AlreadyExists(self)
        query = """
        INSERT INTO ingredient (id, unit, ingredient_type, suggestion_threshold, rebuy_threshold, durability)
        VALUES (%s, %s, %s, %s, %s, %s)"""
        db.insert(query, self.name, self.unit, self.type, self.suggestion_threshold, self.rebuy_threshold,
                  self.durability)

    def in_stock(self) -> float:
        """
        Counts total of amount left in table stock for ingredient
        
        :return:    How much is left in stock
        """
        query = """
        SELECT count(amount_left) AS amount
        FROM stock
        WHERE ingredient = %s
        """
        res = db.select(query, self.name)
        return res.amount

    def __load_from_db(self):
        query = """
        SELECT unit, ingredient_type, suggestion_threshold, rebuy_threshold, durability
        FROM ingredient
        WHERE id = %s
        """
        res = db.select(query, self.name)
        if not res:
            raise errors.DoesNotExist(Ingredient, identifier=self.name,
                                      add_info='New ingredients should be initiated with keyword new')
        self.unit = res.unit
        self.type = res.ingredient_type
        self.suggestion_threshold = res.suggestion_threshold
        self.rebuy_threshold = res.rebuy_threshold
        self.durability = res.durability
