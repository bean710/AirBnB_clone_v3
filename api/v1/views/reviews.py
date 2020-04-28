#!/usr/bin/python3
"""File for the reviews route"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route("/reviews", methods=["GET"], strict_slashes=False)
def all_reviews():
    """Returns JSON of all of the reviews"""
    return jsonify([v.to_dict() for k, v in storage.all(Review).items()])


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
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

@app_views.route("/reviews", methods=["POST"], strict_slashes=False)
def create_review():
    """Creates a review"""
    data = request.get_json()

    if "name" not in data:
        return "Missing name", 400

    nreview = Review(**data)
    storage.new(nreview)
    storage.save()

    return jsonify(nreview.to_dict()), 201

@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Updates a review"""
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)
    else:
        data = request.get_json(force=True)

        for k, v in data.items():
            if k != "id" and k != "created_at" and k != "updated_at":
                setattr(review, k, v)

        storage.save()
        return jsonify(review.to_dict()), 200
