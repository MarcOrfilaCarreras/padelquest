# -*- coding: utf-8 -*-
import json

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields

from .models import Competition
from .models import ma
from .models import Player
from .models import PlayerRankingHistory
from .models import Tournament
from .models import TournamentResults

db = SQLAlchemy()


class CompetitionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Competition

    id = ma.auto_field()
    name = ma.auto_field()
    url = ma.auto_field()
    last_update = ma.auto_field()


class PlayerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Player

    id = ma.auto_field()
    url = ma.auto_field()

    name = ma.auto_field()
    birth_date = ma.auto_field()
    birth_place = ma.auto_field()
    height = ma.auto_field()
    image = fields.Method("build_image_url")

    ranking = ma.auto_field()
    games = ma.auto_field()
    won_games = ma.auto_field()
    points = ma.auto_field()
    side_position = ma.auto_field()

    teammate_id = ma.auto_field()
    teammate_url = ma.auto_field()

    competition_id = ma.auto_field()

    def build_image_url(self, obj):
        if obj.image:
            return f"{current_app.config['BASE_URL']}/v1/competitions/{obj.competition_id}/player/{obj.id}/image"
        else:
            return None


class TournamentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tournament

    id = ma.auto_field()
    url = ma.auto_field()

    name = ma.auto_field()
    poster = fields.Method("build_poster_url")

    start_date = ma.auto_field()
    end_date = ma.auto_field()

    referees = fields.Method("serialize_referees")

    competition_id = ma.auto_field()

    def serialize_referees(self, obj):
        if obj.referees:
            return json.loads(obj.referees)
        else:
            return None

    def build_poster_url(self, obj):
        if obj.poster:
            return f"{current_app.config['BASE_URL']}/v1/competitions/{obj.competition_id}/tournaments/{obj.id}/image"
        else:
            return None


class TournamentBasicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tournament

    id = ma.auto_field()
    url = ma.auto_field()

    name = ma.auto_field()
    poster = fields.Method("build_poster_url")

    start_date = ma.auto_field()
    end_date = ma.auto_field()

    competition_id = ma.auto_field()

    def build_poster_url(self, obj):
        if obj.poster:
            return f"{current_app.config['BASE_URL']}/v1/competitions/{obj.competition_id}/tournaments/{obj.id}/image"
        else:
            return None


class TournamentResultSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TournamentResults

    id = ma.auto_field()
    round = ma.auto_field()
    court = ma.auto_field()

    player1_couple1_id = ma.auto_field()
    player2_couple1_id = ma.auto_field()
    player1_couple2_id = ma.auto_field()
    player2_couple2_id = ma.auto_field()

    first_set = ma.auto_field()
    second_set = ma.auto_field()
    third_set = ma.auto_field()

    not_presented = ma.auto_field()

    tournament_id = ma.auto_field()

    competition_id = ma.auto_field()


class PlayerRankingHistorySchema(ma.SQLAlchemySchema):
    class Meta:
        model = PlayerRankingHistory

    ranking = ma.auto_field()
    date = ma.auto_field()
