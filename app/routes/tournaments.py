# -*- coding: utf-8 -*-
import datetime
import json

from flask import make_response
from flask import request
from models.models import Tournament
from models.models import TournamentResults
from models.schemas import TournamentBasicSchema
from models.schemas import TournamentResultSchema
from models.schemas import TournamentSchema
from sqlalchemy import func


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


def v1CompetitionsTournamentImage(id_competition, id_tournament):
    tournament_schema = TournamentSchema()
    tournament = Tournament.query.filter(
        Tournament.competition_id == id_competition, Tournament.id == id_tournament).first()

    try:
        from app import image_downloader

        image_name = f"competition{id_competition}_tournament{id_tournament}.png"
        image_stream = image_downloader.get_image(
            tournament.poster, image_name)

        headers = {
            'Content-Type': 'image/png'
        }

        return make_response(image_stream, headers)
    except:
        response = {"status": "fail", "data": {
            "message": "Image not found"}}, 206
        return response
