#!/usr/bin/python3
"""File for the states route"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from flasgger import swag_from


@app_views.route("/states", methods=["GET"], strict_slashes=False)
@swag_from("docs/state/all_states.yml")
def all_states():
    """Returns JSON of all of the states
    file: all_states.yml
    """
    return jsonify([v.to_dict() for k, v in storage.all(State).items()])


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
@swag_from("docs/state/get_state.yml")
def get_state(state_id):
    """Returns a specific state"""
    state = storage.get("State", state_id)

    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from("docs/state/del_state.yml")
def del_state(state_id):
    """Deletes a specific state"""
    state = storage.get("State", state_id)

    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
@swag_from("docs/state/create_state.yml")
def create_state():
    """Creates a state"""
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    nstate = State(**data)
    storage.new(nstate)
    storage.save()

    return jsonify(nstate.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
@swag_from("docs/state/update_state.yml")
def update_state(state_id):
    """Updates a state"""
    state = storage.get("State", state_id)

    if state is None:
        abort(404)
    else:
        data = request.get_json(force=True)

        if data is None:
            return jsonify({"error": "Not a JSON"}), 400

        for k, v in data.items():
            if k != "id" and k != "created_at" and k != "updated_at":
                setattr(state, k, v)

        storage.save()
        return jsonify(state.to_dict()), 200
