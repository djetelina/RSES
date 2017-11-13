# coding=utf-8
import logging

from pytest import fixture

from rses.src.objects import stock

logging.basicConfig(level=logging.INFO)


@fixture(params=['D_4.i-R;Y', 'Mléčné výrobky'])
def ingredient_type_name(request):
    return request.param


@fixture(params=['pastry', 'p.4_s -T;r@Y'])
def ingredient_type_new_name(request):
    yield request.param
    try:
        stock.IngredientType.load_by_name(request.param).delete()
    except AttributeError:
        pass


@fixture
def ingredient_type_no_create(ingredient_type_name):
    yield ingredient_type_name
    stock.IngredientType.load_by_name(ingredient_type_name).delete()


@fixture
def ingredient_type(ingredient_type_name):
    IT = stock.IngredientType(name=ingredient_type_name)
    yield IT
    # Reload from database, because tast could have done who knows what with it
    try:
        stock.IngredientType(ingredient_type_id=IT.id).delete()
    # If deleted by test
    except AttributeError:
        pass


@fixture
def ingredient_type_no_delete(ingredient_type_name):
    IT = stock.IngredientType(name=ingredient_type_name)
    yield IT


@fixture(params=['S ug4r;', 'e_g-G.s', 'Petržel'])
def ingredient_name(request):
    return request.param


@fixture(params=['Kusů'])
def ingredient_unit(request):
    return request.param


@fixture(params=[3, 50])
def positive_int(request):
    return request.param


@fixture(params=[3.14532, 2.00016])
def positive_float(request):
    return request.param

positive_float2 = positive_float


@fixture
def ingredient_no_create(ingredient_name):
    yield ingredient_name
    stock.Ingredient.load_by_name(ingredient_name).delete()

