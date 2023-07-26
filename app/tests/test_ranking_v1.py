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


def test_get_single_ranking_v1(client):
    response = client.get('/v1/competitions/1/ranking')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert len(data["data"]) <= 10


def test_get_single_ranking_fail_not_found_v1(client):
    response = client.get('/v1/competitions/100/ranking')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The ranking was not found"
    }
    assert data["data"] == expected_data


def test_get_single_ranking_top_v1(client):
    response = client.get('/v1/competitions/1/ranking?top=50')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert len(data["data"]) <= 50


def test_get_single_ranking_top_fail_v1(client):
    response = client.get('/v1/competitions/1/ranking?top=101')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The maximum number of players is limited to 100"
    }
    assert data["data"] == expected_data


def test_get_single_ranking_top_fail_top_v1(client):
    response = client.get('/v1/competitions/1/ranking?top=')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert len(data["data"]) <= 10
