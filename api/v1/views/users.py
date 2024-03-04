#!/usr/bin/python3
"""USER Api"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """Retrieves all Amenities"""
    users = storage.all(User).values()
    all_users = []
    for user in users:
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves specific user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes specific user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def create_user():
    """Creates a new user"""
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json' or not request.get_json():
        abort(400, 'Not a JSON')

    user_data = request.get_json()
    if 'email' not in user_data:
        abort(400, 'Missing email')
    if 'password' not in user_data:
        abort(400, 'Missing password')
    new_user = User(**user_data)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """Update specific User"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json' or not request.get_json():
        abort(400, 'Not a JSON')

    user_data = request.get_json()
    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in user_data.items():
        if key not in ignored_keys:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
