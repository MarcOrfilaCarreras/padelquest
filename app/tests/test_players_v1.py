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


def test_get_single_player(client):
    response = client.get('/v1/competitions/1/player/2')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert isinstance(data["data"], list)

    expected_id = 2
    assert data["data"][0]["id"] == expected_id

    expected_competition = 1
    assert data["data"][0]["competition_id"] == expected_competition

    expected_name = "Maximiliano Arce Simo"
    assert data["data"][0]["name"] == expected_name


def test_get_single_player_fail_not_found_v1(client):
    response = client.get('/v1/competitions/1/player/0')
    assert response.status_code == 206
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The requested player was not found"
    }
    assert data["data"] == expected_data


def test_get_single_player_fail_no_parameter_v1(client):
    response = client.get('/v1/competitions/1/player/')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The requested URL does not exist"
    }
    assert data["data"] == expected_data


def test_get_single_player_fail_image_v1(client):
    response = client.get('/v1/competitions/1/player/0/image')
    assert response.status_code == 206
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "Image not found"
    }
    assert data["data"] == expected_data
