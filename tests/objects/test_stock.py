# coding=utf-8
from pytest import raises

from rses.src.objects import stock
import rses_errors


def test_ingredient_type_create(ingredient_type_no_create):
    ingredient_type = stock.IngredientType(name=ingredient_type_no_create)
    assert ingredient_type.id
    assert ingredient_type.name == ingredient_type_no_create


def test_ingredient_type_rename(ingredient_type, ingredient_type_new_name):
    ingredient_type.name = ingredient_type_new_name
    assert ingredient_type.name == ingredient_type_new_name
    new = stock.IngredientType(ingredient_type_id=ingredient_type.id)
    assert new.name == ingredient_type_new_name
    assert ingredient_type == new


def test_ingredient_type_delete(ingredient_type):
    ingredient_type.delete()
    with raises(rses_errors.DoesNotExist) as e:
        stock.IngredientType.load_by_name(ingredient_type.name)
    assert ingredient_type.name in str(e)


def test_ingredient_create(ingredient_type,
                           ingredient_no_create,
                           ingredient_unit,
                           positive_float,
                           positive_float2,
                           positive_int):
    """
    In arguments, ingredient_type has to come before ingredient_no_create,
    otherwise teardown of ingredient_type will come first and will cascade
    delete ingredient_unit
    """
    ingredient = stock.Ingredient(name=ingredient_no_create,
                                  unit=ingredient_unit,
                                  ingredient_type=ingredient_type,
                                  suggestion_threshold=positive_float,
                                  rebuy_threshold=positive_float2,
                                  durability=positive_int)
    assert ingredient.name == ingredient_no_create
    assert ingredient.unit == ingredient_unit
    assert ingredient.type == ingredient_type
    assert ingredient.suggestion_threshold == positive_float
    assert ingredient.rebuy_threshold == positive_float2
    assert ingredient.durability == positive_int
