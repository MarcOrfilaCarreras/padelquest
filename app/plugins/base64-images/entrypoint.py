# -*- coding: utf-8 -*-
import base64
import json

import yaml
from flask import Blueprint
from flask import request
from flask import Response

from .config import ENABLED

# Create the blueprint for the plugin
plugin_blueprint = Blueprint('base64-images', __name__)


@plugin_blueprint.after_app_request
def return_base64(response):
    """
    Convert the response content to base64 format.

    :param response: The response object from the request.
    :return: The response object.
    """

    if not (response.headers.get('Content-Type') == "image/png"):
        return response

    if not (request.args.get("format") and (request.args.get("format") == "base64")):
        return response

    image_data = response.get_data()

    encoded_image = base64.b64encode(image_data).decode('utf-8')

    response.set_data(encoded_image)

    return response


def register_plugin(app):
    """
    Register the plugin's blueprint with the Flask app.

    :param app: The Flask app instance.
    """

    # Register the blueprint with the app
    if ENABLED:
        app.register_blueprint(plugin_blueprint)
