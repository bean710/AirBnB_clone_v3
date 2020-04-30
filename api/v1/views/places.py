#!/usr/bin/python3
"""File for the places route"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from os import getenv


storage_t = getenv("HBNB_TYPE_STORAGE")


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def all_places(city_id):
    """Returns JSON of all of the places"""
    city = storage.get("City", city_id)

    if city is None:
        abort(404)

    if storage_t == "db":
        return jsonify([place.to_dict() for place in city.places])
    else:
        a_places = storage.all(Place).values()
        places = [place.to_dict() for place in a_places
                  if place.city_id == city_id]
        return jsonify(places)


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


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a place"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    user = storage.get("User", data["user_id"])
    if user is None:
        abort(404)

    data["city_id"] = city_id
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

        if data is None:
            return jsonify({"error": "Not a JSON"}), 400

        for k, v in data.items():
            if k not in ("id", "user_id", "city_id", "created_at",
                         "updated_at"):
                setattr(place, k, v)

        storage.save()
        return jsonify(place.to_dict()), 200
