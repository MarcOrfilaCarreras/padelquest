# -*- coding: utf-8 -*-
import json

import msgpack
from flask import Blueprint
from flask import request
from flask import Response

from .config import ENABLED

# Create the blueprint for the plugin
plugin_blueprint = Blueprint('format-messagepack', __name__)


@plugin_blueprint.after_app_request
def return_messagepack(response):
    """
    Convert the response content to MessagePack format.

    :param response: The response object from the request.
    :return: The response object.
    """

    if not (request.args.get("format") and (request.args.get("format") == "messagepack")):
        return response

    if not response.is_json:
        return response

    data = json.loads(response.get_data(as_text=True))
    messagepack_data = msgpack.packb(data)
    hex_representation = " ".join([f"{x:02X}" for x in messagepack_data])

    # Create a new Response object with the MessagePack content
    messagepack_response = Response(hex_representation)
    messagepack_response.status_code = response.status_code

    messagepack_response.headers.pop('Content-Type', 'application/messagepack')

    return messagepack_response


def register_plugin(app):
    """
    Register the plugin's blueprint with the Flask app.

    :param app: The Flask app instance.
    """

    # Register the blueprint with the app
    if ENABLED:
        app.register_blueprint(plugin_blueprint)
