# coding=utf-8
"""Objects related to ingredients and stock"""
import logging
from typing import Union, List, Any

from psycopg2 import sql

import errors
from connections import db

log = logging.getLogger(__name__)


class IngredientType:
    """For shopping list organization and filtering"""
    def __init__(self, *, ingredient_type_id: Union[int, None]=None, name: Union[str, None]=None) -> None:
        log.debug('Init of %s', repr(self))
        self._id: Union[int, None] = ingredient_type_id
        self._name: Union[str, None] = name
        if not self._id:
            self.create()
        elif not self._name:
            self.__load_from_db()

    def __str__(self):
        return f"Ingredient type '{self.name}'"

    def __repr__(self):
        return f'IngredientType(id={self.id}, name={self.name})'

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        log.debug("Updating name of %, new name: %s", str(self), new_name)
        query = """
        UPDATE ingredient_type
        SET name = %s
        WHERE id = %s
        """
        db.update(query, new_name, self._id)
        self._name = new_name

    def exists(self) -> bool:
        """Whether the ingredient type exists"""
        query = """
        SELECT * 
        FROM ingredient_type
        WHERE name = %s
        """
        res = db.select(query, self._name)
        return bool(res)

    def create(self):
        """Creates an ingredient type"""
        log.debug('Trying to create new %s', str(self))
        if self.exists() or self._id:
            raise errors.AlreadyExists(self)
        query = """
        INSERT INTO ingredient_type (name)
        VALUES (%s)
        RETURNING id
        """
        self._id = db.insert(query, self._name).id
        log.debug('Created, new id: %s', self.id)

    def delete(self):
        """Deletes an ingredient type"""
        log.debug('Deleting %s', str(self))
        if not self.exists():
            raise errors.DoesNotExist(IngredientType, identifier=self._name)
        query = """
        DELETE FROM ingredient_type
        WHERE id = %s
        """
        db.delete(query, self._id)

    def items(self) -> List[Ingredient]:
        """All ingredients of this type"""
        log.debug('Getting all ingredients of %s', str(self))
        query = """
        SELECT id as id
        FROM ingredient
        WHERE ingredient_type = %s
        """
        res = db.select_all(query, self._id)
        ingredients = list()
        for item in res:
            ingredients.append(Ingredient(ingredient_id=item.id))
        return ingredients

    def __load_from_db(self):
        """Loads ingredient type from the database"""
        query = """
        SELECT name
        FROM ingredient_type
        WHERE id = %s
        """
        res = db.select(query, self._id)
        self._name = res.name


class Ingredient:
    """An ingredient to buy and use in recipes"""
    def __init__(
            self, *,
            ingredient_id: Union[int, None]=None,
            name: Union[str, None]=None,
            unit: Union[str, None] = None,
            ingredient_type: Union[IngredientType, None] = None,
            suggestion_threshold: Union[float, None] = 0.0,
            rebuy_threshold: Union[float, None] = 0.0,
            durability: Union[int, None] = None
    ) -> None:
        """
        :param ingredient_id:                      Identifier for an ingredient, assigned be the database on creation
        :param name:                    The name of the ingredient, as will be display everywhere
        :param unit:                    The measurable unit of the ingredient, can be virtually anything
        :param ingredient_type:         The type if ingredient that the item belongs to
        :param suggestion_threshold:    When the shopping system will recommend you to maybe purchase
        :param rebuy_threshold:         When the shopping system tells you to absolutely buy it next time you see it
        :param durability:              If specified, calculates the expiration date based on the date of purchase
        """
        self._id: Union[int, None] = ingredient_id
        self._name: str = name
        self._unit: Union[str, None] = unit
        self._type: Union[IngredientType, None] = ingredient_type
        self._suggestion_threshold: Union[float, None] = suggestion_threshold
        self._rebuy_threshold: Union[float, None] = rebuy_threshold
        self._durability: Union[int, None] = durability
        if not self._id:
            self.create()
        else:
            self.__load_from_db()

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = self.__updater('name', new_name)

    @property
    def unit(self) -> str:
        return self._unit

    @unit.setter
    def unit(self, new_unit):
        self._unit = self.__updater('unit', new_unit)

    @property
    def type(self) -> IngredientType:
        return self._type

    @type.setter
    def type(self, new_type: IngredientType):
        self.__updater('type', new_type.id)
        self._type = new_type

    @property
    def suggestion_threshold(self) -> float:
        return self._suggestion_threshold

    @suggestion_threshold.setter
    def suggestion_threshold(self, new_threshold):
        self._suggestion_threshold = self.__updater('suggestion_threshold', new_threshold)

    @property
    def rebuy_threshold(self) -> float:
        return self._suggestion_threshold

    @rebuy_threshold.setter
    def rebuy_threshold(self, new_threshold):
        self._rebuy_threshold = self.__updater('rebuy_threshold', new_threshold)

    @property
    def durability(self) -> int:
        return self._durability

    @durability.setter
    def durability(self, new_durability):
        self._durability = self.__updater('durability', new_durability)

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
        return db.select(query, self._name).average

    def __str__(self):
        return self._name

    def __repr__(self):
        return f'Ingredient(name={self._name}, unit={self._unit}, type={repr(self._type)}, ' \
               f'suggestion_threshold={self._suggestion_threshold}, rebuy_threshold={self._rebuy_threshold}'

    def exists(self) -> bool:
        """
        :return:    If the ingredient exists
        """
        query = """
        SELECT * 
        FROM ingredient
        WHERE name = %s
        """
        res = db.select(query, self._name)
        return bool(res)

    def create(self):
        """
        Creates the ingredient, requires to have type and unit specified.
        
        Default thresholds are 0 and no durability is set.
        """
        required_params = dict(type=self._type, unit=self._unit)
        for name, param in required_params:
            if param is None:
                errors.MissingParameter(name)
        if self.exists():
            raise errors.AlreadyExists(self)
        query = """
        INSERT INTO ingredient (name, unit, ingredient_type, suggestion_threshold, rebuy_threshold, durability)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id"""
        self._id = db.insert(query, self._name, self._unit, self._type.id, self._suggestion_threshold,
                             self._rebuy_threshold, self._durability).id

    def remove_stock(self, amount: float) -> None:
        """Removes amount of ingredient from the stock, from the oldest"""
        query_select = """
        SELECT id, amount_left
        FROM stock
        WHERE amount_left > 0
        ORDER BY time_bought DESC
        LIMIT 1
        """
        res = db.select(query_select)
        can_remove = res.amount_left if res.amount_left >= amount else amount
        query_update = """
        UPDATE stock
        SET amount_left = amount_left - %s
        WHERE id = %s
        """
        db.delete(query_update, res.id)
        amount -= can_remove
        # FIXME > instead of != in case an error happened somewhere, after testing this, it can be replaced
        if amount > 0:
            self.remove_stock(amount)

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
        res = db.select(query, self._id)
        return res.amount

    def __updater(self, column, new_value) -> Any:
        """Updates the Ingredient entry's value for specified column"""
        log.debug('Updating ingredient column %s from %s to %s', column, getattr(self, 'column'), new_value)
        query = sql.SQL("""
        UPDATE ingredient
        SET {} = %s
        WHERE id = %s
        """).format(sql.Identifier(column))
        db.update(query, new_value, self._id)
        return new_value


    def __load_from_db(self):
        """Loads the ingredient from the database"""
        query = """
        SELECT unit, ingredient_type, suggestion_threshold, rebuy_threshold, durability
        FROM ingredient
        WHERE id = %s
        """
        res = db.select(query, self._id)
        self._unit = res.unit
        self._type = IngredientType(ingredient_type_id=res.ingredient_type)
        self._suggestion_threshold = res.suggestion_threshold
        self._rebuy_threshold = res.rebuy_threshold
        self._durability = res.durability
