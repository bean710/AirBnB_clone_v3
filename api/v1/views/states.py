#!/usr/bin/python3
"""File for the states route"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """Returns JSON of all of the states"""
    return jsonify([v.to_dict() for k, v in storage.all(State).items()])


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """Returns a specific state"""
    state = storage.get("State", state_id)

    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())
