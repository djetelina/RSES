# coding=utf-8
"""API for more than just one client"""
import html
from urllib.parse import unquote

from flask import Blueprint, json, current_app, session, abort

from objects import stock

rses_api_bp = Blueprint('RSES_API', __name__, url_prefix='/rses/api')


@rses_api_bp.before_request
def before_api_request():
    """Cancels request if the session is not authorized"""
    if not session.get('authorized', False):
        return abort(403)


@rses_api_bp.route('/')
def index():
    """Index page with documentation to the API or endpoints, who knows, for now this"""
    ret = '<h1>Docs or something</h1>'
    for rule in current_app.url_map.iter_rules():
        ret += f"<p>{repr(rule).replace('<', '&lt;').replace('>', '&gt;')}</p>"
    return ret


@rses_api_bp.route('/ingredient_type/<int:ingredient_type_id>', methods=['GET'])
def ingredient_type_get(ingredient_type_id: int):
    """Fetches an ingredient type"""
    try:
        ingredient_type = stock.IngredientType(ingredient_type_id=ingredient_type_id)
    except AttributeError:  # load from db returns None
        return json.jsonify(dict(status=404)), 404
    return json.jsonify(dict(ingredientType=ingredient_type.json_dict)), 200


@rses_api_bp.route('/ingredient_type/<int:ingredient_type_id>', methods=['DELETE'])
def ingredient_type_delete(ingredient_type_id: int):
    """Deletes an ingredient type"""
    stock.IngredientType(ingredient_type_id=ingredient_type_id).delete()
    return json.jsonify(dict(status='OK')), 202


@rses_api_bp.route('/ingredient_type/new/<string:name>', methods=['POST'])
def ingredient_type_create(name: str):
    """Creates a new ingredient type"""
    name = html.unescape(unquote(name))
    ingredient_type = stock.IngredientType(name=name)
    return json.jsonify(dict(status='OK', id=ingredient_type.id)), 201


@rses_api_bp.route('/ingredient_type/<int:ingredient_type_id>/name/<string:new_name>', methods=['POST'])
def ingredient_type_rename(ingredient_type_id: int, new_name: str):
    """Renames an ingredient type"""
    print(new_name)
    new_name = html.unescape(unquote(new_name))
    print(new_name)
    ingredient_type = stock.IngredientType(ingredient_type_id=ingredient_type_id)
    ingredient_type.name = new_name
    return json.jsonify(dict(status='OK', new_name=ingredient_type.name)), 200


@rses_api_bp.route('/list/ingredient_type/<int:limit>/<int:offset>', methods=['GET'])
@rses_api_bp.route('/list/ingredient_type/<int:limit>/<int:offset>/<string:name_filter>', methods=['GET'])
def list_ingredient_types(limit: int, offset: int, name_filter: str= ''):
    """Lists Ingredient Types"""
    name_filter = html.unescape(unquote(name_filter))
    listing = stock.IngredientTypeListing().show(limit, offset, name_filter)
    return json.jsonify(dict(status='OK', ingredient_types=listing)), 200


@rses_api_bp.route('/list/total/ingredient_type', methods=['GET'])
def total_ingredient_types():
    """Returns total amount of Ingredient Types"""
    total = stock.IngredientTypeListing().total
    return json.jsonify(dict(status='OK', total=total)), 200
