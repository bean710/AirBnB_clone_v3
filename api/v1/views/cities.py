#!/usr/bin/python3


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def retrieve_list_city(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get('State', state_id)

    if state is None:
        abort(404)

    all_cities = storage.all("City").values()
    dict_cities = [c.to_dict() for c in all_cities if c.state_id == state_id]
    return jsonify(dict_cities)


@app_views.route("/cities/<city_id>", methods=["GET"],
                   strict_slashes=False)
def retrieve_city_obj(city_id):
    """Retrieves a City object"""
    city = storage.get("City", city_id)

    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                   strict_slashes=False)
def del_city(city_id):
    """
    Deletes a City Object
    """
    city = storage.get("City", city_id)

    if state is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                   strict_slashes=False)
def create_city(state_id):
    """Creates a City"""
    state = storage.get("State", state_id)

    if state is None:
        abort(404)

    data = request.get_json()

    if data is None:
        return jsonify({"error":"Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error":"Missing name"}), 400

    ncity = City(**data)
    storage.new(nstate)
    storage.save()

    return jsonify(nstate.to_dict()), 201

@app_views.route("/cities/<city_id>", methods=["PUT"],
                   strict_slashes=False)
def update_city(city_id):
    """Updates a City Object"""
    city = storage.get("City", city_id)

    if city is None:
        abort(404)
    else:
        data = request.get_json(force=True)

        if data is None:
            return jsonify({"error":"Not a JSON"})
        for k, v in data.items():
            if k != "id" and k != "created_at" and k != "updated_at":
                setattr(city, k, v)

        storage.save()
        return jsonify(city.to_dict()), 200
