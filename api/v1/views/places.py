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


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def search_place():
    """Searches for a place from any city"""
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    pset = set()

    if "states" in data:
        states_s = [storage.get("State", sid) for sid in data["states"]]
        states = [s for s in states_s if s is not None]
        for state in states:
            for city in state.cities:
                pset.update(set(city.places))

    if "cities" in data:
        cities_s = [storage.get("City", cid) for cid in data["cities"]]
        cities = [c for c in cities_s if c is not None]
        for city in cities:
            for place in city.places:
                if place not in pset:
                    pset.add(place)

    if "amenities" in data:
        amenities = [storage.get("Amenity", aid) for aid in data["amenities"]]
        plist = [p for p in pset if
                 all(am in p.amenities for am in amenities)]
    else:
        plist = list(pset)

    #dict_plist = [storage.get("Place", pl.id).to_dict() for pl in plist]
    dict_plist = [pl.to_dict() for pl in plist]
    for pdict in dict_plist:
        if "amenities" in pdict:
            del pdict["amenities"]
    print(dict_plist)
    return jsonify(dict_plist)
