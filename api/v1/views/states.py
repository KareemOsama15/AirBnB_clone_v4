#!/usr/bin/python3
"""State Api"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """method retrieves state objects in a list"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state_id(state_id):
    """method retrieves state object based on id or 404 if not found"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """method deletes state based on id or 404 if not found"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
    else:
        abort(404)
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    """method create a new state instance"""
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json' or not request.get_json():
        abort(400, 'Not a JSON')
    state_data = request.get_json()
    if 'name' not in state_data:
        abort(400, 'Missing name')

    new_state = State(**state_data)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """method update a state instance based on id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json' or not request.get_json():
        abort(400, 'Not a JSON')

    state_data = request.get_json()
    ignored_attr = ["created_at", "updated_at", "id"]
    for key, value in state_data.items():
        if key not in ignored_attr:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
