# -*- coding: utf-8 -*-
import json

import yaml
from flask import Blueprint
from flask import request
from flask import Response

from .config import ENABLED

# Create the blueprint for the plugin
plugin_blueprint = Blueprint('format-yaml', __name__)


@plugin_blueprint.after_app_request
def return_xml(response):
    """
    Convert the response content to YAML format.

    :param response: The response object from the request.
    :return: The response object.
    """

    if not (request.args.get("format") and (request.args.get("format") == "yaml")):
        return response

    if not response.is_json:
        return response

    data = json.loads(response.get_data(as_text=True))
    yaml_data = yaml.dump(data, default_flow_style=False)

    # Create a new Response object with the YAML content
    yaml_response = Response(yaml_data)
    yaml_response.status_code = response.status_code

    yaml_response.headers.pop('Content-Type', 'application/yaml')

    return yaml_response


def register_plugin(app):
    """
    Register the plugin's blueprint with the Flask app.

    :param app: The Flask app instance.
    """

    # Register the blueprint with the app
    if ENABLED:
        app.register_blueprint(plugin_blueprint)
