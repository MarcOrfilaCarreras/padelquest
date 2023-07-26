# -*- coding: utf-8 -*-
import datetime
import io
import json

import models.extras as Extras
import requests
from config import Development
from config import Production
from flask import Flask
from flask import make_response
from flask import request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models.models import Competition
from models.models import db
from models.models import ma
from models.models import Player
from models.models import PlayerTemp
from models.models import Tournament
from models.models import TournamentResults
from models.schemas import CompetitionSchema
from models.schemas import PlayerSchema
from models.schemas import TournamentBasicSchema
from models.schemas import TournamentResultSchema
from models.schemas import TournamentSchema
from sqlalchemy import func

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


@app.route('/v1')
def v1():
    response = {
        "data": {
            "competitions": [
                {
                    "url": "/v1/competitions",
                    "description": "This endpoint returns a list of all competitions."
                },
                {
                    "url": "/v1/competition{competition_id}",
                    "description": "Retrieves the details of a specific competition by its ID. By default, it returns competition 1."
                },
                {
                    "url": "/v1/competition{competition_id}/ranking",
                    "description": "Returns a list of players in a competition, sorted by their ranking. By default, it returns the first 10 players."
                },
                {
                    "url": "/v1/competition{competition_id}/search",
                    "description": "Searches for players in a competition by name and side position. By default, it returns the players with the name of Juan."
                }
            ],
            "players": [
                {
                    "url": "/v1/competition{competition_id}/player/{player_id}",
                    "description": "Retrieves the details of a specific player in a competition by their ID. By default, it returns player 1 of competition 1."
                },
                {
                    "url": "/v1/competition{competition_id}/player/{player_id}/image",
                    "description": "This API route returns the image of a specific player in a given competition."
                }
            ],
            "tournaments": [
                {
                    "url": "/v1/competition{competition_id}/tournaments",
                    "description": "Returns the tournaments of a competition. By default, it returns the current year."
                },
                {
                    "url": "/v1/competition{competition_id}/tournaments/{tournament_id}",
                    "description": "Returns the results of a tournament."
                },
                {
                    "url": "/v1/competition{competition_id}/tournaments/{tournament_id}/image",
                    "description": "Returns the poster of a tournament."
                }
            ]
        },
        "status": "success"
    }

    return response


@app.route('/v1/competitions')
def v1Competitions():
    competition_schema = CompetitionSchema(many=True)
    all_competitions = Competition.query.all()

    if all_competitions == None:
        response = {"status": "fail", "data": {
            "message": "Competitions not found"}}, 206
    else:
        response = {"status": "success",
                    "data": competition_schema.dump(all_competitions)}

    return response


@app.route('/v1/competitions/<id_competition>')
def v1CompetitionsId(id_competition=1):
    competition_schema = CompetitionSchema()
    all_competitions = Competition.query.get(id_competition)

    if all_competitions == None:
        response = {"status": "fail", "data": {
            "message": "The requested competition was not found"}}, 206
    else:
        response = {"status": "success",
                    "data": competition_schema.dump(all_competitions)}

    return response


@app.route('/v1/competitions/<id_competition>/player/<id_player>')
def v1CompetitionsPlayerId(id_competition, id_player):
    player_schema = PlayerSchema(many=True)
    players = Player.query.filter(
        Player.competition_id == id_competition, Player.id == id_player).all()

    if len(players) == 0:
        response = {"status": "fail", "data": {
            "message": "The requested player was not found"}}, 206
    else:
        response = {"status": "success", "data": player_schema.dump(players)}

    return response


@app.route('/v1/competitions/<id_competition>/player/<id_player>/image')
def v1CompetitionsPlayerImage(id_competition, id_player):
    player_schema = PlayerSchema()
    players = Player.query.filter(
        Player.competition_id == id_competition, Player.id == id_player).first()

    try:
        response = requests.get(players.image)
        if (response.status_code == 206) or (response.status_code == 200):
            image_stream = io.BytesIO(response.content)

            headers = {
                'Content-Type': 'image/png'
            }

            return make_response(image_stream.getvalue(), headers)
        else:
            response = {"status": "fail", "data": {
                "message": "Image not found"}}, 206
            return response
    except:
        response = {"status": "fail", "data": {
            "message": "Image not found"}}, 206
        return response


@app.route('/v1/competitions/<id_competition>/player/<id_player>/tournaments')
def v1CompetitionsPlayerTournaments(id_competition, id_player):
    tournament_results_schema = TournamentResults()
    tournament_results = TournamentResults.query.filter(
        (TournamentResults.competition_id == id_competition) & (
            (TournamentResults.player1_couple1_id == id_player) |
            (TournamentResults.player2_couple1_id == id_player) |
            (TournamentResults.player1_couple2_id == id_player) |
            (TournamentResults.player2_couple2_id == id_player)
        )
    ).group_by(TournamentResults.tournament_id).all()

    if len(tournament_results) == 0:
        response = {"status": "fail", "data": {
            "message": "The tournaments were not found"}}, 206
    else:
        data = []

        tournament_schema = TournamentBasicSchema()

        for tournament_result in tournament_results:
            tournaments = Tournament.query.filter(
                Tournament.id == tournament_result.tournament_id).first()

            data.append(tournament_schema.dump(tournaments))

        response = {"status": "success", "data": data}

    return response


@app.route('/v1/competitions/<id_competition>/search')
def v1CompetitionsSearchName(id_competition):
    name = username = request.args.get('name', default='Juan', type=str)
    side_position = username = request.args.get('side', default=None, type=str)

    player_schema = PlayerSchema(many=True)

    if (name == "") and (side_position == ""):
        response = {"status": "fail", "data": {
            "message": "The search was unsuccessful"}}, 206
    else:
        query = query.filter(Player.name.contains(
            name), Player.competition_id == id_competition)

        if side_position:
            query = query.filter(Player.side_position.contains(side_position))

        players = query.all()

        if len(players) == 0:
            response = {"status": "fail", "data": {
                "message": "The search was unsuccessful"}}, 206
        else:
            response = {"status": "success",
                        "data": player_schema.dump(players)}

    return response


@app.route('/v1/competitions/<id_competition>/ranking')
def v1CompetitionsRanking(id_competition):
    top = request.args.get('top', default=10, type=int)

    if top <= 100:

        player_schema = PlayerSchema(many=True)
        players = Player.query.filter(Player.competition_id == id_competition, Player.ranking > 0).order_by(
            Player.ranking).limit(top).all()

        if len(players) == 0:
            response = {"status": "fail", "data": {
                "message": "The ranking was not found"}}, 206
        else:
            response = {"status": "success",
                        "data": player_schema.dump(players)}

    else:
        response = {"status": "fail", "data": {
            "message": "The maximum number of players is limited to 100"}}, 400

    return response


@app.route('/v1/competitions/<id_competition>/tournaments')
def v1CompetitionsTournaments(id_competition):
    year = request.args.get(
        'year', default=datetime.date.today().year, type=int)

    tournament_schema = TournamentBasicSchema(many=True)
    tournaments = Tournament.query.filter(Tournament.competition_id == id_competition, func.extract(
        'year', Tournament.start_date) == year).all()

    if len(tournaments) == 0:
        response = {"status": "fail", "data": {
            "message": "The tournaments were not found"}}, 206
    else:
        response = {"status": "success",
                    "data": tournament_schema.dump(tournaments)}

    return response


@app.route('/v1/competitions/<id_competition>/tournaments/<id_tournament>')
def v1CompetitionsTournament(id_competition, id_tournament):
    tournament_schema = TournamentBasicSchema()
    tournament = Tournament.query.filter(
        Tournament.competition_id == id_competition, Tournament.id == id_tournament).first()

    if not tournament:
        response = {"status": "fail", "data": {
            "message": "The tournament was not found"}}, 206
    else:
        response = {"status": "success",
                    "data": tournament_schema.dump(tournament)}

    return response


@app.route('/v1/competitions/<id_competition>/tournaments/<id_tournament>/results')
def v1CompetitionsTournamentsResults(id_competition, id_tournament):
    if id_competition != "2":
        round = request.args.get('round', default=None, type=str)
        court = request.args.get('court', default=None, type=str)

        query = TournamentResults.query.filter(
            TournamentResults.competition_id == id_competition,
            TournamentResults.tournament_id == id_tournament
        )

        if round:
            query = query.filter(
                TournamentResults.round == round)
        if court:
            query = query.filter(
                TournamentResults.court == court)

        results = query.all()

        if len(results) == 0:
            response = {"status": "fail", "data": {
                "message": "The results were not found"}}, 206
        else:
            results_schema = TournamentResultSchema(many=True)
            response = {"status": "success",
                        "data": results_schema.dump(results)}
    else:
        response = {"status": "fail", "data": {
            "message": "This competition does not allow to obtain the results of the matches"}}, 206

    return response


@app.route('/v1/competitions/<id_competition>/tournaments/<id_tournament>/referees')
def v1CompetitionsTournamentsReferees(id_competition, id_tournament):
    tournament_schema = TournamentSchema()
    tournament = Tournament.query.filter(
        Tournament.competition_id == id_competition, Tournament.id == id_tournament).first()

    if not tournament or (tournament.referees == None):
        response = {"status": "fail", "data": {
            "message": "The referees were not found"}}, 206
    else:
        response = {"status": "success",
                    "data": json.loads(tournament.referees)}

    return response


@app.route('/v1/competitions/<id_competition>/tournaments/<id_tournament>/image')
def v1CompetitionsTournamentImage(id_competition, id_tournament):
    tournament_schema = TournamentSchema()
    tournament = Tournament.query.filter(
        Tournament.competition_id == id_competition, Tournament.id == id_tournament).first()

    try:
        response = requests.get(tournament.poster)

        if (response.status_code == 200) or (response.status_code == 206):
            image_stream = io.BytesIO(response.content)

            headers = {
                'Content-Type': 'image/png'
            }

            return make_response(image_stream.getvalue(), headers)
        else:
            response = {"status": "fail", "data": {
                "message": "Image not found"}}, 206
            return response
    except:
        response = {"status": "fail", "data": {
            "message": "Image not found"}}, 206
        return response


@app.errorhandler(404)
def page_not_found(error):
    return {"status": "fail", "data": {"message": "The requested URL does not exist"}}, 404


if __name__ == '__main__':
    app.run()
