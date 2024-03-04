#!/usr/bin/python3
"""City Api"""
from flask import make_response, jsonify, abort, request
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_state_cities(state_id):
    """method that gets all citeies related to specific state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = []
    for city in state.cities:
        if city.state_id == state_id:
            cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """method gets city based on id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """method deletes a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """method craetes a new city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json' or not request.get_json():
        abort(400, 'Not a JSON')

    city_data = request.get_json()
    if 'name' not in city_data:
        abort(400, 'Missing name')

    new_city = City(**city_data)
    new_city.state_id = state_id
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """updates a city instance"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json' or not request.get_json():
        abort(400, 'Not a JSON')

    city_data = request.get_json()
    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in city_data.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
