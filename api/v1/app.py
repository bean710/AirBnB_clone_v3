#!/usr/bin/python3
"""
API status module
"""

from flask import Flask, jsonify, make_response
from flasgger import Swagger
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
swagger = Swagger(app)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(self):
    """
    Closes the storage
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """
    Handles page not found (Error 404)
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    # TODO: MAKE THE DEBUG FALSE
    app.run(host=host, port=port, threaded=True)
