#!/usr/bin/python3


from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage

@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)

@app_views.route()("/cities/<city_id>", methods=["GET"],
                   strict_slashes=False)

@app_views.route()("/cities/<city_id>", methods=["DELETE"],
                   strict_slashes=False)

@app_views.route()("/states/<state_id>/cities", methods=["POST"],
                   strict_slashes=False)

@app_views.route()("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)

