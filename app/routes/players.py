# -*- coding: utf-8 -*-
from flask import make_response
from models.models import Player
from models.models import Tournament
from models.models import TournamentResults
from models.schemas import PlayerSchema
from models.schemas import TournamentBasicSchema


def v1CompetitionsPlayerId(id_competition, id_player):
    player_schema = PlayerSchema(many=True)
    players = Player.query.filter(
        Player.competition_id == id_competition, Player.id == id_player).all()

    if len(players) == 0:
        response = {"status": "fail", "data": {
            "message": "The requested player was not found"}}, 206

        return response

    response = {"status": "success", "data": player_schema.dump(players)}

    return response


def v1CompetitionsPlayerImage(id_competition, id_player):
    player_schema = PlayerSchema()
    players = Player.query.filter(
        Player.competition_id == id_competition, Player.id == id_player).first()

    try:
        from app import image_downloader

        image_name = f"competition{id_competition}_player{id_player}.png"
        image_stream = image_downloader.get_image(players.image, image_name)

        headers = {
            'Content-Type': 'image/png'
        }

        return make_response(image_stream, headers)
    except:
        response = {"status": "fail", "data": {
            "message": "Image not found"}}, 206
        return response


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

        return response

    data = []

    tournament_schema = TournamentBasicSchema()

    for tournament_result in tournament_results:
        tournaments = Tournament.query.filter(
            Tournament.id == tournament_result.tournament_id).first()

        data.append(tournament_schema.dump(tournaments))

    response = {"status": "success", "data": data}

    return response
