#!/usr/bin/python3
"""File for the states route"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.amenity import Amenity
from flasgger import swag_from
from os import getenv


storage_t = getenv("HBNB_TYPE_STORAGE")


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def all_place_amenitiesplace_id(place_id):
    """Returns JSON of all of the amenities in a place"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    if storage_t == "db":
        return jsonify([a.to_dict() for a in place.amenities])
    else:
        alist = storage.all(Amenity)
        return jsonify([a.to_dict() for a in alist
                        if a.id in place.amenity_ids])


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def del_place_amenity(place_id, amenity_id):
    """Deletes an amenity from a place"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    if storage_t == "db":
        if amenity_id not in {a.id for a in place.amenities}:
            abort(404)

        new_ams = [a for a in place.amenities if a.id != amenity_id]
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)

        new_ams = [a for a in place.amenity_ids if a != amenity_id]

    place.amenities = new_ams
    storage.save()

    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def link_to_place(place_id, amenity_id):
    """Links an amenity to a place"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)

    if amenity_id in {am.id for am in place.amenities}:
        return jsonify(amenity.to_dict()), 200
    else:
        place.amenities.append(amenity if storage_t == "db" else amenity_id)
        storage.save()
        return jsonify(amenity.to_dict()), 201
