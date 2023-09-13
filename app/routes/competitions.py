# -*- coding: utf-8 -*-
from flask import request
from models.models import Competition
from models.models import Player
from models.schemas import CompetitionSchema
from models.schemas import PlayerSchema


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


def v1CompetitionsSearchName(id_competition):
    name = request.args.get('name', default='Juan', type=str)
    side_position = request.args.get('side', default=None, type=str)

    player_schema = PlayerSchema(many=True)

    if (name == "") and (side_position == ""):
        response = {"status": "fail", "data": {
            "message": "The search was unsuccessful"}}, 206
    else:
        query = Player.query.filter(Player.name.contains(
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
