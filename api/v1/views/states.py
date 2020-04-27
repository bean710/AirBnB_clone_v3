#!/usr/bin/python3
"""File for the states route"""


from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """Returns JSON of all of the states"""
    return jsonify([v.to_dict() for k, v in storage.all().items()])


@app_views.route("/states/<state_id>", methods)
