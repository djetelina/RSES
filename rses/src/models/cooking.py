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
        query = """
        SELECT * 
        FROM recipe_category
        WHERE id = %s
        """
        res = db.select(query, self.name)
        return bool(res)

    def create(self):
        if self.exists():
            raise errors.AlreadyExists(self)
        query = """
        INSERT INTO recipe_category (id)
        VALUES (%s)
        """
        db.insert(query, self.name)

    def delete(self):
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
    def __init__(
            self,
            name: str,
            directions: str = '',
            picture: Union[str, None] = None,
            prepare_time: Union[int, None] = None,
            portions: int = 1,
            new: bool = False
    ):
        self.name = name
        self.directions = directions
        self.picture = picture
        self.prepare_time = prepare_time
        self.portions = portions
        self.ingredients: List[Dict[Ingredient, float]] = []
        self.categories: List[RecipeCategory] = []
        if not new:
            self.__load_from_db()

    def add_ingredient(self, ingredient: Ingredient, amount: float):
        for d in self.ingredients:
            if d in d.keys():
                # TODO second parameter of error to show relation
                raise errors.AlreadyExists(ingredient)
        query = """
        INSERT INTO recipe_ingredients (recipe, ingredient, amount) 
        VALUES (%s, %s, %s)
        """
        db.insert(query, self.name, ingredient.name, amount)
        self.ingredients.append({ingredient: amount})

    def remove_ingredient(self, ingredient: Ingredient):
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
        if category in self.categories:
            # TODO second parameter of error to show relation
            raise errors.AlreadyExists(category)
        query = """
        INSERT INTO categorized_recipes (recipe, category) 
        VALUES (%s, %s)
        """
        db.insert(query, self.name, category.name)
        self.categories.append(category)

    def remove_category(self, category: RecipeCategory):
        query = """
        DELETE FROM categorized_recipes
        WHERE recipe = %s
        AND category = %s
        """
        db.delete(query, self.name, category.name)

    def __load_from_db(self):
        # TODO continue here
        pass
