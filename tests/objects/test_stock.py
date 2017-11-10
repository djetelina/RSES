# coding=utf-8
from pytest import mark

from rses.src.objects import stock


def test_ingredient_type_create(ingredient_type_no_create):
    ingredient_type = stock.IngredientType(name=ingredient_type_no_create)
    assert ingredient_type.id
    assert ingredient_type.name == ingredient_type_no_create


@mark.parametrize('new_name', ['pastry', 'P4S tRy', 'p.4_s-T;r@Y'])
def test_ingredient_type_rename(ingredient_type, new_name):
    ingredient_type.name = new_name
    assert ingredient_type.name == new_name
    new = stock.IngredientType(ingredient_type_id=ingredient_type.id)
    assert new.name == new_name
    assert ingredient_type == new


def test_ingredient_type_load():
    pass


def test_ingredient_type_delete():
    pass
