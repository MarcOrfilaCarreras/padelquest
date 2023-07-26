# -*- coding: utf-8 -*-
import io
import json

import pytest
from flask import Flask

from app import app
# Import your Flask app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_single_competition_tournament_v1(client):
    response = client.get('/v1/competitions/1/tournaments')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert len(data["data"]) > 0


def test_get_single_competition_tournament_fail_not_found_v1(client):
    response = client.get('/v1/competitions/100/tournaments')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "fail"

    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The tournaments were not found"
    }
    assert data["data"] == expected_data


def test_get_single_competition_tournament_year_v1(client):
    response = client.get('/v1/competitions/1/tournaments?year=2022')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert len(data["data"]) > 0


def test_get_single_competition_tournament_year_fail_v1(client):
    response = client.get('/v1/competitions/1/tournaments?year=2000')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The tournaments were not found"
    }
    assert data["data"] == expected_data


def test_get_single_competition_tournament_results_fail_url_v1(client):
    response = client.get('/v1/competitions/1/tournaments/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The requested URL does not exist"
    }
    assert data["data"] == expected_data


def test_get_single_competition_tournament_results_fail_not_found_v1(client):
    response = client.get('/v1/competitions/1/tournaments/0')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The results were not found"
    }
    assert data["data"] == expected_data


def test_get_single_competition_tournament_results_v1(client):
    response = client.get('/v1/competitions/1/tournaments/1001')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert len(data["data"]) > 0


def test_get_single_competition_tournament_results_round_v1(client):
    response = client.get('/v1/competitions/1/tournaments/1001?round=R16')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert len(data["data"]) > 0


def test_get_single_competition_tournament_results_round_fail_empty_v1(client):
    response = client.get('/v1/competitions/1/tournaments/1001?round=')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert len(data["data"]) > 0


def test_get_single_competition_tournament_results_round_fail_empty_v1(client):
    response = client.get('/v1/competitions/1/tournaments/1001?round=TEST')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The results were not found"
    }
    assert data["data"] == expected_data


def test_get_single_competition_tournament_court_round_v1(client):
    response = client.get('/v1/competitions/1/tournaments/1022?court=CTR.')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert len(data["data"]) > 0


def test_get_single_competition_tournament_court_round_fail_empty_v1(client):
    response = client.get('/v1/competitions/1/tournaments/1022?court=')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert len(data["data"]) > 0


def test_get_single_competition_tournament_court_round_fail_empty_v1(client):
    response = client.get('/v1/competitions/1/tournaments/1022?court=TEST')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The results were not found"
    }
    assert data["data"] == expected_data
