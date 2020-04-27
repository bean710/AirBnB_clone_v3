#!/usr/bin/python3
"""File for the places route"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route("/places", methods=["GET"], strict_slashes=False)
def all_places():
    """Returns JSON of all of the places"""
    return jsonify([v.to_dict() for k, v in storage.all(Place).items()])


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Returns a specific place"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_place(place_id):
    """Deletes a specific place"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

@app_views.route("/places", methods=["POST"], strict_slashes=False)
def create_place():
    """Creates a place"""
    data = request.get_json()

    if "name" not in data:
        return "Missing name", 400

    nplace = Place(**data)
    storage.new(nplace)
    storage.save()

    return jsonify(nplace.to_dict()), 201

@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a place"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)
    else:
        data = request.get_json(force=True)

        for k, v in data.items():
            if k != "id" and k != "created_at" and k != "updated_at":
                setattr(place, k, v)

        storage.save()
        return jsonify(place.to_dict()), 200
