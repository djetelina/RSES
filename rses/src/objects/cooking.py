# coding=utf-8
"""Objects related to cooking"""
from typing import List, Optional, Dict, Any
import logging

from psycopg2 import sql

import rses_errors
from rses_connections import db
from objects.stock import Ingredient

log = logging.getLogger(__name__)


class RecipeCategory:
    """
    For recipe categorization
    """

    def __init__(self, *, recipe_category_id: Optional[int] = None, name: Optional[str] = None) -> None:
        self._id: Optional[int] = recipe_category_id
        self._name: Optional[str] = name
        if not self._id:
            self.create()
        elif not self._name:
            self.__load_from_db()

    def __str__(self):
        return f'Recipe Category {self._name}'

    def __repr__(self):
        return f'RecipeCategory(id={self._id}, name={self._name})'

    @property
    def id(self) -> int:
        """Id of the recipe category in the database, cannot be changed"""
        return self._id

    @property
    def name(self) -> str:
        """Name of the recipe category"""
        return self._name

    @name.setter
    def name(self, new_name: str):
        log.debug("Updating name of %s, new name: %s", str(self), new_name)
        query = """
        UPDATE recipe_category
        SET name = %s
        WHERE id = %s
        """
        db.update(query, new_name, self._id)
        self._name = new_name

    def exists(self) -> bool:
        """Checks whether the recipe category exists"""
        query = """
        SELECT * 
        FROM recipe_category
        WHERE name = %s
        """
        res = db.select(query, self._name)
        if res:
            log.debug('%s was found in the database', self._name)
        else:
            log.debug('%s was not found in the database', self._name)
        return bool(res)

    def create(self) -> None:
        """Creates the recipe category"""
        if self.exists() or self._id:
            raise rses_errors.AlreadyExists(self)
        if self._name is None:
            raise rses_errors.MissingParameter('name')
        query = """
        INSERT INTO recipe_category (id, name)
        VALUES (DEFAULT, %s)
        RETURNING *
        """
        self._id = db.insert(query, self._name).id
        log.debug('Created, new id: %s', self.id)

    def delete(self) -> None:
        """Deletes the recipe category"""
        if not self.exists():
            raise rses_errors.DoesNotExist(RecipeCategory, identifier=self._name)
        query = """
        DELETE FROM recipe_category
        WHERE id = %s
        """
        db.delete(query, self._id)

    def items(self) -> List['Recipe']:
        """All ingredients of this type"""
        query = """
        SELECT recipe
        FROM categorized_recipes
        WHERE category = %s
        """
        res = db.select_all(query, self._id)
        recipes = list()
        for item in res:
            recipes.append(Recipe(recipe_id=item.id))
        return recipes

    def __load_from_db(self):
        """Loads recipe category from database"""
        query = """
        SELECT name
        FROM recipe_category
        WHERE id = %s"""
        res = db.select(query, self._id)
        self._name = res.name


class Recipe:
    """A recipe object"""
    def __init__(
            self, *,
            recipe_id: Optional[int] = None,
            name: Optional[str] = None,
            directions: str = '',
            picture: Optional[str] = None,
            prepare_time: Optional[int] = None,
            portions: Optional[int] = None
    ) -> None:
        """
        :param name:            Name of the recipe
        :param directions:      How to make it :)
        :param picture:         Picture of the finished thing
        :param prepare_time:    Prepare time in minutes
        :param portions:        For how many portions should the recipe be shown
        """
        self._id: Optional[int] = recipe_id
        self._name: Optional[str] = name
        self._directions: str = directions
        self._picture: Optional[str] = picture
        self._prepare_time: Optional[int] = prepare_time
        self._portions: Optional[int] = portions
        self.ingredients: Dict[Ingredient, float] = dict()
        self.categories: List[RecipeCategory] = list()
        if not self._id:
            self.create()
        else:
            self.__load_from_db()
        self._wanted_portions = self._portions

    @property
    def id(self) -> int:
        """Id of the recipe in the database"""
        return self._id

    @property
    def name(self) -> str:
        """Name of the recipe as shown to the user"""
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = self.__updater('name', new_name)

    @property
    def directions(self) -> str:
        """How to make the recipe into a meal :)"""
        return self._directions

    @directions.setter
    def directions(self, new_directions: str):
        self._directions = self.__updater('directions', new_directions)

    @property
    def picture(self) -> str:
        """URL of an image of the recipe, saved somewhere else, this will not be stored in the database!"""
        return self._picture

    @picture.setter
    def picture(self, new_picture_link: str):
        self._picture = self.__updater('picture', new_picture_link)

    @property
    def prepare_time(self) -> Optional[int]:
        """The time in minutes it takes to prepare the meal, this is optional"""
        return self._prepare_time

    @prepare_time.setter
    def prepare_time(self, new_time: int):
        self._prepare_time = self.__updater('prepare_time', new_time)

    @property
    def portions(self) -> int:
        """For how many people the recipe is written for, can be recalculated but not through this property!"""
        return self._portions

    @portions.setter
    def portions(self, new_amount: int):
        self._portions = self.__updater('portions', new_amount)

    @property
    def wanted_portions(self) -> int:
        """For how many portions the ingredients are being shown"""
        return self._wanted_portions

    @wanted_portions.setter
    def wanted_portions(self, new_amount: int):
        new_ratio: float = self._wanted_portions / new_amount
        self._wanted_portions: int = new_amount
        for ingredient, amount in self.ingredients.items():
            self.ingredients[ingredient] = amount * new_ratio

    @property
    def portion_price(self) -> float:
        """Price of a single portion based on ingredient average"""
        return self.current_price / self._portions

    @property
    def current_price(self) -> float:
        """Price of the whole meal based on ingredient average"""
        price: float = 0.0
        for ingredient, amount in self.ingredients.items():
            price += ingredient.average_price * amount
        return price

    def create(self) -> None:
        """Creates the recipe, has to be created before ingredients and categories are added!"""
        required_params = dict(portions=self._portions, name=self._name)
        for name, param in required_params.items():
            if param is None:
                raise rses_errors.MissingParameter(name)
        query = """
        INSERT INTO recipe (name, directions, picture, prepare_time, portions) 
        VALUES (%s, %s, %s, %s, %s)
        """
        db.insert(query, self._name, self._directions, self._picture, self._prepare_time, self._portions)

    def delete(self) -> None:
        """Deletes the recipe"""
        query = """
        DELETE FROM recipe
        WHERE id = %s
        """
        db.delete(query, self._name)

    def add_ingredient(self, ingredient: Ingredient, amount: float) -> None:
        """Adds an ingredient to the recipe"""
        if ingredient in self.ingredients.keys():
            raise rses_errors.AlreadyExists(ingredient, relation=self)
        query = """
        INSERT INTO recipe_ingredients (recipe, ingredient, amount) 
        VALUES (%s, %s, %s)
        """
        db.insert(query, self._id, ingredient.id, amount)
        self.ingredients[ingredient] = amount

    def remove_ingredient(self, ingredient: Ingredient) -> None:
        """Removes an ingredient from the recipe"""
        query = """
        DELETE FROM recipe_ingredients
        WHERE ingredient = %s 
        AND recipe = %s
        """
        db.delete(query, ingredient.id, self._id)
        self.ingredients.pop(ingredient, None)

    def add_category(self, category: RecipeCategory) -> None:
        """Adds the recipe into a category"""
        if category in self.categories:
            raise rses_errors.AlreadyExists(category, relation=self)
        query = """
        INSERT INTO categorized_recipes (recipe, category) 
        VALUES (%s, %s)
        """
        db.insert(query, self._id, category.id)
        self.categories.append(category)

    def remove_category(self, category: RecipeCategory) -> None:
        """Removes the recipe from a category"""
        query = """
        DELETE FROM categorized_recipes
        WHERE recipe = %s
        AND category = %s
        """
        db.delete(query, self._id, category.id)

    def can_be_cooked(self) -> bool:
        """Checks whether the recipe can be cooked"""
        for ingredient, amount in self.ingredients.items():
            if amount > ingredient.in_stock:
                return False
        return True

    def cook(self) -> None:
        """Adds the recipe the a log of cooked recipes and subtracts the ingredients from stock"""
        if not self.can_be_cooked():
            raise rses_errors.NotEnoughIngredients
        query = """
        INSERT INTO recipe_made (recipe, portions, price) 
        VALUES (%s, %s, %s)
        """
        db.insert(query, self._id, self._portions, self.current_price)
        for ingredient, amount in self.ingredients.items():
            ingredient.remove_stock(amount)

    def __load_from_db(self) -> None:
        """Loads the recipe, it's ingredients and categories from the database"""
        query = """
        SELECT name, directions, picture, prepare_time, portions
        FROM recipe
        WHERE id = %s
        """
        res = db.select(query, self._id)
        self._name = res.name
        self._directions = res.directions
        self._picture = res.picture
        self._prepare_time = res.prepare_time
        self._portions = res.portions

        query_ingredients = """
        SELECT ingredient, amount
        FROM recipe_ingredients
        WHERE recipe = %s
        """
        res = db.select_all(query_ingredients, self._id)
        for i in res:
            ingredient = Ingredient(ingredient_id=i.ingredient)
            self.ingredients[ingredient] = res.amount
        query_categories = """
        SELECT category
        FROM categorized_recipes
        WHERE recipe = %s
        """
        res = db.select_all(query_categories, self._id)
        for category in res:
            self.categories.append(RecipeCategory(recipe_category_id=category.category))

    def __updater(self, column: str, new_value: Any) -> Any:
        """Updates the Ingredient entry's value for specified column"""
        log.debug('Updating recipe column %s from %s to %s', column, getattr(self, 'column'), new_value)
        query = sql.SQL("""
        UPDATE recipe
        SET {} = %s
        WHERE id = %s
        """).format(sql.Identifier(column))
        db.update(query, new_value, self._id)
        return new_value
