# -*- coding: utf-8 -*-
import json

from flask import Blueprint
from flask import request
from flask import Response
from json2xml import json2xml

from .config import ENABLED

# Create the blueprint for the plugin
plugin_blueprint = Blueprint('format-xml', __name__)


@plugin_blueprint.after_app_request
def return_xml(response):
    """
    Convert the response content to xml format.

    :param response: The response object from the request.
    :return: The response object.
    """

    if not (request.args.get("format") and (request.args.get("format") == "xml")):
        return response

    if not response.is_json:
        return response

    data = json.loads(response.get_data(as_text=True))

    xml_string = json2xml.Json2xml(
        data, wrapper="root", pretty=True, attr_type=False).to_xml()

    # Create a new Response object with the XML content
    xml_response = Response(xml_string, content_type='application/xml')
    xml_response.status_code = response.status_code

    return xml_response


def register_plugin(app):
    """
    Register the plugin's blueprint with the Flask app.

    :param app: The Flask app instance.
    """

    # Register the blueprint with the app
    if ENABLED:
        app.register_blueprint(plugin_blueprint)
