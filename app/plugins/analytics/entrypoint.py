# -*- coding: utf-8 -*-
import datetime
import os

from flask import abort
from flask import Blueprint
from flask import request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import ENABLED
from .config import ENABLED_API
from .models.models import Day
from .models.models import URL
from .models.schemas import URLSchema

# Create the engine and session
engine = create_engine(
    f'sqlite:///{os.path.dirname(os.path.abspath(__file__))}/analytics.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

# Create the blueprint
plugin_blueprint = Blueprint('plugin', __name__)


def create_analytics(routes):
    """
    Create or update URL and Day entries in the database based on the given routes.

    :param routes: List of routes to be analyzed for analytics.
    """
    # Use URL.metadata directly to create the URL table
    URL.metadata.create_all(engine)
    # Use URL.metadata directly to create the Day table
    Day.metadata.create_all(engine)

    for route in routes:
        # Check if the URL already exists in the database
        existing_url = session.query(URL).get(route)

        # If the URL doesn't exist, add it to the database
        if not existing_url:
            url = URL(name=route)
            session.add(url)

    # Commit the changes to the database
    session.commit()


@plugin_blueprint.after_app_request
def save_analytics(response):
    """
    Save analytics data after each request if analytics is enabled.

    :param response: The response object from the request.
    :return: The response object.
    """
    if ENABLED:
        try:
            url = request.url_rule.rule

            # Retrieve the URL entry from the database
            url_entry = session.query(URL).get(url)
            if url_entry:
                # Update the URL visit count
                url_entry.total_visits += 1

                # Check and update the Day entry for today's date
                day_entry = session.query(Day).filter(
                    Day.url_id == url_entry.name, Day.date == datetime.date.today()).first()

                if day_entry is None:
                    # If there is no Day entry for today, create a new one
                    day = Day(datetime.datetime.today(), url_entry.name, 0)
                    session.add(day)

                # Retrieve the Day entry again (it may have been created just above)
                day_entry = session.query(Day).filter(
                    Day.url_id == url_entry.name, Day.date == datetime.date.today()).first()

                if day_entry is not None:
                    # Update the Day entry visit count for today
                    day_entry.total_visits += 1

                # Commit the changes to the database
                session.commit()
        except:
            pass

    return response


@plugin_blueprint.route('/plugins/analytics')
def get_analytics():
    """
    Get the analytics data from the database and return it as a JSON response.

    :return: JSON response containing the analytics data.
    """
    if ENABLED_API:
        url_schema = URLSchema(many=True)

        urls = session.query(URL).all()

        if len(urls) == 0:
            response = {"status": "fail", "data": {
                "message": "Analytics were not found"}}, 206

        else:
            # Serialize the URL objects using the URLSchema and return the data as JSON
            return {"status": "success", "data": url_schema.dump(urls)}
    else:
        # If the analytics API is not enabled, return a 404 error
        return abort(404)


def register_plugin(app):
    """
    Register the plugin's blueprint with the Flask app and create/update analytics data.

    :param app: The Flask app instance.
    """

    if ENABLED:
        routes = [rule.rule for rule in app.url_map.iter_rules()
                  if 'static' not in rule.endpoint]
        create_analytics(routes)

    app.register_blueprint(plugin_blueprint)

    if ENABLED:
        routes = [rule.rule for rule in app.url_map.iter_rules()
                  if 'static' not in rule.endpoint]
        create_analytics(routes)
