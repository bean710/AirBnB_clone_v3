#!/usr/bin/python3
"""File for the amenities route"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def all_amenities():
    """Returns JSON of all of the amenities"""
    return jsonify([v.to_dict() for _, v in storage.all(Amenity).items()])


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Returns a specific amenity"""
    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """Deletes a specific amenity"""
    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates an amenity"""
    data = request.get_json()

    if "name" not in data:
        return "Missing name", 400

    namenity = Amenity(**data)
    storage.new(namenity)


@app_views.route("/amenity/<amenity_id>", methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a amenity"""
    amenity = storage.get("State", amenity_id)

    if amenity is None:
        abort(404)
    else:
        data = request.get_json(force=True)

        if data is None:
            return jsonify({"error": "Not a JSON"}), 400

        for k, v in data.items():
            if k != "id" and k != "created_at" and k != "updated_at":
                setattr(amenity, k, v)

        storage.save()
        return jsonify(amenity.to_dict()), 200
