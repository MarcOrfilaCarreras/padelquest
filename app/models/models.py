# -*- coding: utf-8 -*-
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import Sequence
from sqlalchemy import String
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

db = SQLAlchemy()
ma = Marshmallow()


class Competition(db.Model):
    __tablename__ = 'competitions'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50))
    url = Column(String(200))
    last_update = Column(Date)

    @staticmethod
    def insert_default_competitions():
        default_competitions = [
            {'id': 1, 'name': 'A1 Padel Global',
                'url': 'https://www.a1padelglobal.com/'},
            {'id': 2, 'name': 'Premier Padel', 'url': 'https://premierpadel.com/'},
            {'id': 3, 'name': 'World Padel Tour',
                'url': 'https://worldpadeltour.com/'},
        ]

        for competition in default_competitions:
            if Competition.query.filter_by(id=competition['id']).first() is None:
                db.session.add(Competition(**competition))

        db.session.commit()


class Player(db.Model):
    __tablename__ = 'players'

    id = Column(Integer, Sequence('players_id'), primary_key=False, autoincrement=True,
                server_default=Sequence('players_id').next_value(), nullable=False, unique=True)
    url = Column(String(300), primary_key=True)

    name = Column(String(200))
    birth_date = Column(Date)
    birth_place = Column(String(100))
    height = Column(Integer)
    image = Column(String(200))

    ranking = Column(Integer)
    games = Column(Integer)
    won_games = Column(Integer)
    points = Column(Integer)
    side_position = Column(String(50))

    teammate_id = Column(Integer, ForeignKey('players.id'))
    teammate_url = Column(String(300))

    competition_id = Column(Integer, ForeignKey('competitions.id'))

    teammate = relationship('Player')
    competition = relationship('Competition')


class PlayerTemp(db.Model):
    __tablename__ = 'players_temp'

    url = Column(String(300), primary_key=True)
    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, unique=True)


class Tournament(db.Model):
    __tablename__ = 'tournaments'

    id = Column(Integer, Sequence('tournaments_id'), primary_key=False, autoincrement=True,
                server_default=Sequence('tournaments_id').next_value(), nullable=False, unique=True)
    url = Column(String(300), primary_key=True)

    name = Column(String(200))
    poster = Column(String(300))

    start_date = Column(Date)
    end_date = Column(Date)

    referees = Column(String(300), nullable=True)

    competition_id = Column(Integer, ForeignKey('competitions.id'))
    competition = relationship('Competition')


class TournamentResults(db.Model):
    __tablename__ = 'tournaments_results'

    id = Column(Integer, Sequence('tournament_results_id'), primary_key=False, autoincrement=True,
                server_default=Sequence('tournament_results_id').next_value(), nullable=False, unique=True)

    round = Column(String(75))
    court = Column(String(300))

    date = Column(Date)

    url_player1_couple1 = Column(String(200), nullable=True)
    url_player2_couple1 = Column(String(300), nullable=True)
    url_player1_couple2 = Column(String(200), nullable=True)
    url_player2_couple2 = Column(String(300), nullable=True)

    player1_couple1_id = Column(Integer, ForeignKey('players.id'))
    player2_couple1_id = Column(Integer, ForeignKey('players.id'))
    player1_couple2_id = Column(Integer, ForeignKey('players.id'))
    player2_couple2_id = Column(Integer, ForeignKey('players.id'))

    first_set = Column(String(300), nullable=True)
    second_set = Column(String(300), nullable=True)
    third_set = Column(String(300), nullable=True)

    not_presented = Column(Boolean, nullable=True)

    url_tournament = Column(String(200))
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))
    competition = relationship('Tournament')

    competition_id = Column(Integer, ForeignKey('competitions.id'))
    competition = relationship('Competition')

    # Define composite primary key
    __table_args__ = (
        PrimaryKeyConstraint('url_player1_couple1',
                             'url_player1_couple2', 'round', 'url_tournament'),
    )


class PlayerRankingHistory(db.Model):
    __tablename__ = 'players_ranking_history'

    id = Column(Integer, primary_key=True)

    ranking = Column(Integer)
    date = Column(DateTime, server_default=func.now())

    player_id = Column(Integer, ForeignKey('players.id'))

    player = relationship('Player')
