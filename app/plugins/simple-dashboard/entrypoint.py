# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import render_template
from models.models import Competition
from models.models import Player
from models.models import Tournament
from models.models import TournamentResults

from .config import ENABLED

# Create the blueprint for the plugin
plugin_blueprint = Blueprint(
    'simple-dashboard', __name__, static_folder='static', template_folder='templates')


@plugin_blueprint.route('/plugins/dashboard')
def get_dashboard():
    if ENABLED:
        num_competitions = Competition.query.count()
        num_players = Player.query.count()
        num_tournaments = Tournament.query.count()
        num_results = TournamentResults.query.count()

        return render_template("index.html", num_competitions=num_competitions, num_players=num_players, num_tournaments=num_tournaments, num_results=num_results)
    else:
        # If the dashboard is not enabled, return a 404 error
        return abort(404)


def register_plugin(app):
    """
    Register the plugin's blueprint with the Flask app.

    :param app: The Flask app instance.
    """

    # Register the blueprint with the app
    if ENABLED:
        app.register_blueprint(plugin_blueprint)
