#!/usr/bin/python3


from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def retrieve_list_city():
    """
    Retrieves the list of all City objects of a State
    """


@app_views.route("/cities/<city_id>", methods=["GET"],
                   strict_slashes=False)
def retrieve_city_obj():
    """
    Retrieves a City object
    """


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                   strict_slashes=False)
def del_city():
    """
    Deletes a City Object
    """


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                   strict_slashes=False)
def create_city():
    """
    Creates a City
    """


@app_views.route("/cities/<city_id>", methods=["PUT"],
                   strict_slashes=False)
def update_city():
    """
    Updates a City Object
    """
