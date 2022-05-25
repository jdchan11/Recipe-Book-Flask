from crypt import methods
import token
from tokenize import Token
from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, User, Recipe, recipe_schema, recipes_schema
from flask_cors import cross_origin

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/recipes', methods = ['POST'])
@token_required
def create_recipe(current_user_token):
    recipe_title = request.json['recipe_title']
    prep_time = request.json['prep_time']
    cook_time = request.json['cook_time']
    ingredients = request.json['ingredients']
    recipe_instructions = request.json['recipe_instructions']
    user_token = current_user_token.token

    recipe = Recipe(recipe_title, prep_time, cook_time, ingredients, recipe_instructions, user_token = user_token)

    db.session.add(recipe)
    db.session.commit()

    response = recipe_schema.dump(recipe)
    return jsonify(response)

@api.route('/recipes', methods = ['GET'])
@token_required
def get_recipes(current_user_token):
    recipes = Recipe.query.filter_by(user_token = current_user_token.token).all()
    response = recipes_schema.dump(recipes)
    return jsonify(response)

@api.route('/recipes/<id>', methods = ['GET'])
@token_required
def get_recipe(current_user_token, id):
    recipe = Recipe.query.get(id)
    response = recipe_schema.dump(recipe)
    return jsonify(response)

@api.route('/recipes/<id>', methods = ['POST', 'PUT'])
@token_required
def update_recipe(current_user_token, id):
    recipe = Recipe.query.get(id)
    recipe.recipe_title = request.json['recipe_title']
    recipe.prep_time = request.json['prep_time']
    recipe.cook_time = request.json['cook_time']
    recipe.ingredients = request.json['ingredients']
    recipe.recipe_instructions = request.json['recipe_instructions']
    recipe.user_token = current_user_token.token

    db.session.commit()
    response = recipe_schema.dump(recipe)
    return jsonify(response)

@api.route('/recipes/<id>', methods = ['DELETE'])
@token_required
def delete_recipe(current_user_token, id):
    recipe = Recipe.query.get(id)
    db.session.delete(recipe)
    db.session.commit()
    response = recipe_schema.dump(recipe)
    return jsonify(response)

@api.route('/recipes/<id>', methods = ['OPTIONS'])
def options_check(id):
    recipe = Recipe.query.get(id)
    response = recipe_schema.dump(recipe)
    return jsonify(response) 