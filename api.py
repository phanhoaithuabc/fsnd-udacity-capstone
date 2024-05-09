import os
from flask import Flask, request, jsonify, redirect
import json
from flask_cors import CORS

from models import create_db_with_data, setup_db, Food
from auth import AuthError, requires_auth

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = ['RS256']
API_AUDIENCE = os.environ.get('API_AUDIENCE')
CLIENT_ID = os.environ.get('CLIENT_ID')

# api = Blueprint('api', __name__)
app = Flask(__name__)
with app.app_context():
    setup_db(app)
    CORS(app)
    # create_db_with_data()

# ROUTES

@app.route('/login')
def login():
    return redirect('https://' + AUTH0_DOMAIN + '/authorize?audience=' + API_AUDIENCE + \
                    '&response_type=token&client_id=' + CLIENT_ID + '&redirect_uri=' + \
                        request.host_url + 'foods')

@app.route('/foods', methods=['GET'])
@requires_auth('get:foods')
def get_all_foods(payload):
    try:
        foods = Food.query.order_by(Food.id).all()
        result = [food.just_title() for food in foods]
        return jsonify({
            'success': True,
            'foods': result
        })
    except Exception as e:
        print("error", e)
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/foods-ingredient', methods=['GET'])
@requires_auth('get:foods-ingredient')
def get_foods_detail(payload):
    try:
        foods = Food.query.order_by(Food.id).all()
        result = list()
        for food in foods:
            result.append(food.full_version())
        return jsonify({
            'success': True,
            'foods': result
        })
    except Exception as e:
        print("error", e)
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/foods', methods=['POST'])
@requires_auth('post:foods')
def create_food(payload):
    try:
        body = request.get_json()
        title = body.get('title')
        ingredient = body.get('ingredient')
        if not (title and ingredient):
            raise ValueError('Invalid request body')
        
        new_food = Food(title=title, ingredient=json.dumps(ingredient))
        new_food.insert()
        
        return jsonify({
            'success': True,
            'food': [new_food.full_version()]
        })
    except (KeyError, TypeError, ValueError) as e:
        print("error", e)
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/foods/<int:food_id>', methods=['PATCH'])
@requires_auth('patch:foods')
def update_food(payload, food_id):
    try:
        body = request.get_json()
        if not body:
            raise ValueError('Request doesnt have valid JSON body')
        
        food_to_update = Food.query.get(food_id)
        if not food_to_update:
            raise ValueError('No foods found')
        
        title = body.get('title')
        ingredient = body.get('ingredient')
        if title:
            food_to_update.title = title
        if ingredient:
            food_to_update.ingredient = ingredient
        food_to_update.update()
        
        return jsonify({
            'success': True,
            'food': food_to_update.full_version()
        })
    except (KeyError, TypeError, ValueError, Exception) as e:
        print("error", e)
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/foods/<int:food_id>', methods=['DELETE'])
@requires_auth('delete:foods')
def delete_food(payload, food_id):
    try:
        food_to_delete = Food.query.get(food_id)
        if not food_to_delete:
            raise ValueError('Food ID {} not found'.format(food_id))
        
        food_to_delete.delete()
        
        return jsonify({
            'success': True,
            'delete': food_id
        })
    except (ValueError, Exception) as e:
        print("error", e)
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
    }), 404


@app.errorhandler(AuthError)
def authentication_failed(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": "Authentication Failed"
    }), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)