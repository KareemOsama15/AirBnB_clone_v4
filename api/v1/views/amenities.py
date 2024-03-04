#!/usr/bin/python3
"""Amenity Api"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """Retrieves all Amenities"""
    amenties = storage.all(Amenity).values()
    all_amenities = []
    for amenity in amenties:
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves specific amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes specific amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def create_amenity():
    """Creates a new amenity"""
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json' or not request.get_json():
        abort(400, 'Not a JSON')

    amenity_data = request.get_json()
    if 'name' not in amenity_data:
        abort(400, 'Missing name')
    new_amenity = Amenity(**amenity_data)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update specific Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json' or not request.get_json():
        abort(400, 'Not a JSON')

    amenity_data = request.get_json()
    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in amenity_data.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
