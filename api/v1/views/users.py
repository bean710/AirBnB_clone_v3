#!/usr/bin/python3
"""File for the users route"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def all_users():
    """Returns JSON of all of the users"""
    return jsonify([v.to_dict() for k, v in storage.all(User).items()])


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Returns a specific user"""
    user = storage.get("User", user_id)

    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_user(user_id):
    """Deletes a specific user"""
    user = storage.get("User", user_id)

    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a user"""
    data = request.get_json()

    if "name" not in data:
        return "Missing name", 400

    nuser = User(**data)
    storage.new(nuser)
    storage.save()

    return jsonify(nuser.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Updates a user"""
    user = storage.get("User", user_id)

    if user is None:
        abort(404)
    else:
        data = request.get_json(force=True)

        for k, v in data.items():
            if k != "id" and k != "created_at" and k != "updated_at":
                setattr(user, k, v)

        storage.save()
        return jsonify(user.to_dict()), 200
