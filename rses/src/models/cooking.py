# coding=utf-8
"""Objects related to cooking"""
from typing import List, Union, Dict

import errors
from connections import db
from models.stock import Ingredient


class RecipeCategory:
    """
    For recipe categorization
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'RecipeCategory(name={self.name})'

    def exists(self) -> bool:
        """Checks whether the recipe category exists"""
        query = """
        SELECT * 
        FROM recipe_category
        WHERE id = %s
        """
        res = db.select(query, self.name)
        return bool(res)

    def create(self):
        """Creates the recipe category"""
        if self.exists():
            raise errors.AlreadyExists(self)
        query = """
        INSERT INTO recipe_category (id)
        VALUES (%s)
        """
        db.insert(query, self.name)

    def delete(self):
        """Deletes the recipe category"""
        if not self.exists():
            raise errors.DoesNotExist(RecipeCategory, identifier=self.name)
        query = """
        DELETE FROM recipe_category
        WHERE id = %s
        """
        db.delete(query, self.name)

    def items(self) -> List[Ingredient]:
        """All ingredients of this type"""
        query = """
        SELECT recipe
        FROM categorized_recipes
        WHERE category = %s
        """
        res = db.select_all(query, self.name)
        recipes = list()
        for item in res:
            recipes.append(Recipe(item["id"]))
        return recipes


class Recipe:
    """A recipe object"""
    def __init__(
            self,
            name: str,
            directions: str = '',
            picture: Union[str, None] = None,
            prepare_time: Union[int, None] = None,
            portions: int = 1,
            new: bool = False
    ):
        """
        :param name:            Name of the recipe
        :param directions:      How to make it :)
        :param picture:         Picture of the finished thing
        :param prepare_time:    Prepare time in minutes
        :param portions:        How many portions does the recipe counts with
        :param new:             If it's a new recipe, so it doesn't try and load from database
        """
        self.name: str = name
        self.directions: str = directions
        self.picture: Union[str, None] = picture
        self.prepare_time: Union[int, None] = prepare_time
        self.portions: int = portions
        self.ingredients: List[Dict[Ingredient, float]] = []
        self.categories: List[RecipeCategory] = []
        if not new:
            self.__load_from_db()

    def add_ingredient(self, ingredient: Ingredient, amount: float):
        """Adds an ingredient to the recipe"""
        for d in self.ingredients:
            if d in d.keys():
                raise errors.AlreadyExists(ingredient, relation=self)
        query = """
        INSERT INTO recipe_ingredients (recipe, ingredient, amount) 
        VALUES (%s, %s, %s)
        """
        db.insert(query, self.name, ingredient.name, amount)
        self.ingredients.append({ingredient: amount})

    def remove_ingredient(self, ingredient: Ingredient):
        """Removes an ingredient from the recipe"""
        query = """
        DELETE FROM recipe_ingredients
        WHERE ingredient = %s 
        AND recipe = %s
        """
        db.delete(query, ingredient.name, self.name)
        for d in self.ingredients:
            if ingredient in d.keys():
                self.ingredients.remove(d)
                break

    def add_category(self, category: RecipeCategory):
        """Adds the recipe into a category"""
        if category in self.categories:
            raise errors.AlreadyExists(category, relation=self)
        query = """
        INSERT INTO categorized_recipes (recipe, category) 
        VALUES (%s, %s)
        """
        db.insert(query, self.name, category.name)
        self.categories.append(category)

    def remove_category(self, category: RecipeCategory):
        """Removes the recipe from a category"""
        query = """
        DELETE FROM categorized_recipes
        WHERE recipe = %s
        AND category = %s
        """
        db.delete(query, self.name, category.name)

    def __load_from_db(self):
        query = """
        SELECT directions, picture, prepare_time, portions
        FROM recipe
        WHERE id = %s
        """
        res = db.select(query, self.name)
        self.directions = res['directions']
        self.picture = res['picture'],
        self.prepare_time = res['prepare_time']
        self.portions = res['portions']
        query_ingredients = """
        SELECT ingredient, amount
        FROM recipe_ingredients
        WHERE recipe = %s
        """
        res = db.select_all(query_ingredients, self.name)
        for i in res:
            ingredient = Ingredient(i['ingredient'])
            self.ingredients.append({ingredient: i['amount']})
        query_categories = """
        SELECT category
        FROM categorized_recipes
        WHERE recipe = %s
        """
        res = db.select_all(query_categories, self.name)
        for category in res:
            self.categories.append(category['category'])
