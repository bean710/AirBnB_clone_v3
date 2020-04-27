#!/usr/bin/python3
"""
Index module
"""


from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage



@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """
    Returns a JSON status
    """
    return jsonify({"status": "OK"})

@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    """
    Returns JSON of the number of each class
    """
    stats = {}
    stats["amenities"] = storage.count("Amenity")
    stats["cities"] = storage.count("City")
    stats["places"] = storage.count("Place")
    stats["reviews"] = storage.count("Review")
    stats["users"] = storage.count("User")
    return jsonify(stats)
