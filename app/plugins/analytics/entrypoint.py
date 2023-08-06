# -*- coding: utf-8 -*-
import datetime
import os
import re
import threading

from flask import abort
from flask import Blueprint
from flask import request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import ENABLED
from .config import ENABLED_API
from .models.models import Day
from .models.models import URL
from .models.schemas import DaySchema
from .models.schemas import URLSchema

# Create the engine and session for database connection
engine = create_engine(
    f'sqlite:///{os.path.dirname(os.path.abspath(__file__))}/analytics.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

# Create the blueprint for the plugin
plugin_blueprint = Blueprint('plugin', __name__)


def is_valid_date(date_str):
    # Define a regular expression to validate the date format 'YYYY-MM-DD'
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    return re.match(date_pattern, date_str)


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


def save_analytics_thread(url):
    """
    Save analytics data in a separate thread.

    :param url: The URL to update analytics for.
    """
    if ENABLED:
        try:
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
        except Exception as e:
            pass


@plugin_blueprint.after_app_request
def save_analytics(response):
    """
    Save analytics data after each request if analytics is enabled.

    :param response: The response object from the request.
    :return: The response object.
    """

    url = request.url_rule.rule if request.url_rule else None

    thread = threading.Thread(target=save_analytics_thread, args=(url,))
    thread.start()

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
            return response
        else:
            # Serialize the URL objects using the URLSchema and return the data as JSON
            return {"status": "success", "data": url_schema.dump(urls)}
    else:
        # If the analytics API is not enabled, return a 404 error
        return abort(404)


@plugin_blueprint.route('/plugins/analytics/<string:day>')
def get_analytics_by_day(day):
    """
    Get the analytics data from the database and return it as a JSON response for a specific day.

    :param day: The day in 'YYYY-MM-DD' format for which to retrieve analytics.
    :return: JSON response containing the analytics data.
    """
    if ENABLED_API:
        try:
            # Validate the day format before parsing it as a datetime.date object
            if not is_valid_date(day):
                return {"status": "fail", "data": {"message": "Invalid date format. Please use the format YYYY-MM-DD"}}, 400

            # Convert the day from the URL segment to a datetime.date object
            day_date = datetime.datetime.strptime(day, '%Y-%m-%d').date()

            day_schema = DaySchema(many=True)

            day_data = session.query(Day).filter(Day.date == day_date).all()

            if len(day_data) == 0:
                response = {"status": "fail", "data": {
                    "message": "Analytics were not found"}}, 206
                return response
            else:
                # Serialize the URL objects using the URLSchema and return the data as JSON
                return {"status": "success", "data": day_schema.dump(day_data)}
        except Exception as e:
            # Log the exception for debugging purposes
            return {"status": "fail", "data": {"message": "An error occurred while processing the request"}}, 500
    else:
        # If the analytics API is not enabled, return a 404 error
        abort(404)


def register_plugin(app):
    """
    Register the plugin's blueprint with the Flask app and create/update analytics data.

    :param app: The Flask app instance.
    """
    # Create or update analytics data for the routes in the app
    if ENABLED:
        routes = [rule.rule for rule in app.url_map.iter_rules()
                  if 'static' not in rule.endpoint]
        create_analytics(routes)

    # Register the blueprint with the app
    app.register_blueprint(plugin_blueprint)

    # Create or update analytics data again after registration
    if ENABLED:
        routes = [rule.rule for rule in app.url_map.iter_rules()
                  if 'static' not in rule.endpoint]
        create_analytics(routes)
