# coding=utf-8
from pytest import fixture

from rses.src.objects import stock


@fixture(params=['dairy', 'DAIRY', 'DA I RY', 'D_A.I-R;Y', 'd41Ry'])
def ingredient_type_no_create(request):
    yield request.param
    stock.IngredientType.load_by_name(request.param).delete()


@fixture(params=['dairy', 'DAIRY', 'DA I RY', 'D_A.I-R;Y', 'd41Ry'])
def ingredient_type(request):
    ingredient_type = stock.IngredientType(name=request.param)
    yield ingredient_type
    # Reload from database, because tast could have done who knows what with it
    stock.IngredientType(ingredient_type_id=ingredient_type.id).delete()
