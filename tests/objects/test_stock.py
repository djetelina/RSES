# coding=utf-8
from rses.src.objects import stock
from collections import namedtuple

result_id = namedtuple('Result', ['id'])(id=5)
result_name = namedtuple('Result', ['name'])(name='test_ingredient')

def test_ingredient_type_create(mocker, database):
    """Also tests exists()"""
    mocker.patch('psycopg2.connect', database([None, result_id]))
    ingredient_type = stock.IngredientType(name='test_ingredient')
    assert ingredient_type.id == 5
    assert ingredient_type.name == 'test_ingredient'


def test_ingredient_type_rename(mocker, database):
    mocker.patch('psycopg2.connect', database([None, result_id]))
    ingredient_type = stock.IngredientType(name='test_ingredient')
    ingredient_type.name = 'testing_ingredient'
    assert ingredient_type.name == 'testing_ingredient'


def test_ingredient_type_load(mocker, database):
    mocker.patch('psycopg2.connect', database([result_name]))
    ingredient_type = stock.IngredientType(ingredient_type_id=5)
    assert ingredient_type.name == 'test_ingredient'


def test_ingredient_type_delete(mocker, database):
    mocker.patch('psycopg2.connect', database([None, result_id, result_id]))
    ingredient_type = stock.IngredientType(name='test_ingredient')
    ingredient_type.delete()
