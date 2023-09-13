# -*- coding: utf-8 -*-
import importlib
import os

import models.extras as Extras
from config import Development
from config import Production
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models.models import Competition
from models.models import db
from models.models import ma
from routes import competitions
from routes import players
from routes import tournaments
from routes import versions
from utils.cronJobs import ScheduleCronJob
from utils.imageDownloader import ImageDownloader

app = Flask(__name__)
app.config.from_object(Production)
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

    Extras.insert_players_temp()
    Extras.update_teammate_ids()
    Extras.update_tournaments_ids()
    Extras.update_tournaments_results()
    Extras.normalization_names()
    Extras.update_competitions_last_updated()

    Competition.insert_default_competitions()

    image_downloader = ImageDownloader(app.config['IMAGE_FOLDER'])
    schedule_cron_job = ScheduleCronJob(
        app.config['IMAGE_FOLDER'], app.config['CRON_MINUTES'])

    from routes import errors


app.add_url_rule('/v1', view_func=versions.v1)

app.add_url_rule('/v1/competitions', view_func=competitions.v1Competitions)
app.add_url_rule('/v1/competitions/<id_competition>',
                 view_func=competitions.v1CompetitionsId)
app.add_url_rule('/v1/competitions/<id_competition>/search',
                 view_func=competitions.v1CompetitionsSearchName)
app.add_url_rule('/v1/competitions/<id_competition>/ranking',
                 view_func=competitions.v1CompetitionsRanking)

app.add_url_rule('/v1/competitions/<id_competition>/player/<id_player>',
                 view_func=players.v1CompetitionsPlayerId)
app.add_url_rule('/v1/competitions/<id_competition>/player/<id_player>/image',
                 view_func=players.v1CompetitionsPlayerImage)
app.add_url_rule('/v1/competitions/<id_competition>/player/<id_player>/tournaments',
                 view_func=players.v1CompetitionsPlayerTournaments)

app.add_url_rule('/v1/competitions/<id_competition>/tournaments',
                 view_func=tournaments.v1CompetitionsTournaments)
app.add_url_rule('/v1/competitions/<id_competition>/tournaments/<id_tournament>',
                 view_func=tournaments.v1CompetitionsTournament)
app.add_url_rule('/v1/competitions/<id_competition>/tournaments/<id_tournament>/results',
                 view_func=tournaments.v1CompetitionsTournamentsResults)
app.add_url_rule('/v1/competitions/<id_competition>/tournaments/<id_tournament>/referees',
                 view_func=tournaments.v1CompetitionsTournamentsReferees)
app.add_url_rule('/v1/competitions/<id_competition>/tournaments/<id_tournament>/image',
                 view_func=tournaments.v1CompetitionsTournamentImage)

if __name__ == "__main__":
    app.run()
