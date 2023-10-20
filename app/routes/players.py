# -*- coding: utf-8 -*-
from flask import abort
from flask import current_app
from flask import make_response
from flask import request
from models.models import Player
from models.models import PlayerRankingHistory
from models.models import Tournament
from models.models import TournamentResults
from models.schemas import PlayerRankingHistorySchema
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


def v1CompetitionsPlayerRankingHistory(id_competition, id_player):
    history_schema = PlayerRankingHistorySchema(many=True)
    page_size = current_app.config['PAGE_SIZE']

    page = request.args.get('page', default=1, type=int)
    order = request.args.get('order', default="asc", type=str)

    if not (order == "asc" or order == "desc"):
        abort(400)

    total_pages = (PlayerRankingHistory.query.filter(
        PlayerRankingHistory.player_id == id_player).count() + page_size - 1) // page_size

    if order == "asc":
        query = PlayerRankingHistory.query.filter(
            PlayerRankingHistory.player_id == id_player).order_by(PlayerRankingHistory.date.asc())

    if order == "desc":
        query = PlayerRankingHistory.query.filter(
            PlayerRankingHistory.player_id == id_player).order_by(PlayerRankingHistory.date.desc())

    history = query.limit(page_size).offset((page - 1) * page_size).all()

    if len(history) == 0:
        response = {"status": "fail", "data": {
            "message": "The rankings were not found"}}, 206

        return response

    response = {"status": "success", "data": {"meta": {
        "page": page, "page_count": total_pages}, "data": history_schema.dump(history)}}

    return response
