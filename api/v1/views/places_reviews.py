#!/usr/bin/python3
"""File for the reviews route"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def all_reviews(place_id):
    """Returns JSON of all of the reviews"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    reviews = storage.all("Review").values()
    dict_reviews = [r.to_dict() for r in reviews if r.place_id == place_id]
    return jsonify(dict_reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """Returns a specific review"""
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_review(review_id):
    """Deletes a specific review"""
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a review"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    elif "text" not in data:
        return jsonify({"error": "Missing text"}), 400

    user_id = data["user_id"]
    data_user = storage.get("User", user_id)

    if data_user is None:
        abort(404)

    data["place_id"] = place_id
    nreview = Review(**data)
    storage.new(nreview)
    storage.save()

    return jsonify(nreview.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a review"""
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)
    else:
        data = request.get_json(force=True)

        if data is None:
            return jsonify({"error": "Not a JSON"}), 400

        ignore = ["id", "created_at", "place_id", "user_id"]
        for k, v in data.items():
            if k not in ignore:
                setattr(review, k, v)

        storage.save()
        return jsonify(review.to_dict()), 200
