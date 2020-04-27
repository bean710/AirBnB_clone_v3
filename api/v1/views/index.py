#!/usr/bin/python3
"""
Index module
"""

from api.v1.views import app_views
from flask import Flask, jsonify

@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """
    Returns a JSON status
    """
    return jsonify({"status": "OK"})
