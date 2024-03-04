#!/usr/bin/python3
"""Review Api"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.place import Place
from models.user import User
from models.review import Review
from models import storage


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """retrieve list of all reviews of a place"""
    if not storage.get(Place, place_id):
        abort(404)
    reviews = storage.all(Review).values()
    all_reviews = []
    for review in reviews:
        if review.place_id == place_id:
            all_reviews.append(review.to_dict())
    return jsonify(all_reviews)


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieve specific review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a new Place"""
    if not storage.get(Place, place_id):
        abort(404)

    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json' or not request.get_json():
        abort(400, 'Not a JSON')

    review_data = request.get_json()
    if 'user_id' not in review_data:
        abort(400, 'Missing user_id')
    elif not storage.get(User, review_data['user_id']):
        abort(404)
    elif 'text' not in review_data:
        abort(400, 'Missing text')

    review_data['place_id'] = place_id
    new_review = Review(**review_data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update a Review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json' or not request.get_json():
        abort(400, 'Not a JSON')

    review_data = request.get_json()
    ignored_keys = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    for key, value in review_data.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
