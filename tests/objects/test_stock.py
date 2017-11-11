# coding=utf-8
from pytest import mark, raises

from rses.src.objects import stock
import rses_errors


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


def test_ingredient_type_delete(ingredient_type_no_delete):
    ingredient_type_no_delete.delete()
    with raises(rses_errors.DoesNotExist) as e:
        stock.IngredientType.load_by_name(ingredient_type_no_delete.name)
    assert ingredient_type_no_delete.name in str(e)
