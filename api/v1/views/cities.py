#!/usr/bin/python3
"""File for the cities route"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def retrieve_list_city(state_id):
    """Returns JSON of all of the cities"""
    state = storage.get('State', state_id)

    if state is None:
        abort(404)

    all_cities = storage.all("City").values()
    dict_cities = [c.to_dict() for c in all_cities if c.state_id == state_id]
    return jsonify(dict_cities)


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def retrieve_city_obj(city_id):
    """Returns a specific city"""
    city = storage.get("City", city_id)

    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_city(city_id):
    """Deletes a specific City"""
    city = storage.get("City", city_id)

    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a city"""
    state = storage.get("State", state_id)

    if state is None:
        abort(404)

    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    data["state_id"] = state_id
    ncity = City(**data)
    storage.new(ncity)
    storage.save()

    return jsonify(ncity.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a city"""
    city = storage.get("City", city_id)

    if city is None:
        abort(404)
    else:
        data = request.get_json(force=True)

        if data is None:
            return jsonify({"error": "Not a JSON"}), 400

        ignore = ['id', 'created_at', 'state_id']
        for k, v in data.items():
            if k not in ignore:
                setattr(city, k, v)

        storage.save()
        return jsonify(city.to_dict()), 200
