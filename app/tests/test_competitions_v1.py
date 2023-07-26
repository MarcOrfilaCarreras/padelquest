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


def test_get_all_competitions_v1(client):
    response = client.get('/v1/competitions')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert isinstance(data["data"], list)

    expected_data = [
        {
            'id': 1,
            'last_update': None,
            'name': 'A1 Padel Global',
            'url': 'https://www.a1padelglobal.com/'
        },
        {
            'id': 2,
            'last_update': None,
            'name': 'Premier Pádel',
            'url': 'https://premierpadel.com/'
        },
        {
            'id': 3,
            'last_update': None,
            'name': 'World Padel Tour',
            'url': 'https://worldpadeltour.com/'
        }
    ]
    assert data["data"] == expected_data


def test_get_single_competition_v1(client):
    response = client.get('/v1/competitions/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert isinstance(data["data"], dict)

    expected_data = {
        "id": 1,
        "last_update": None,
        "name": "A1 Padel Global",
        "url": "https://www.a1padelglobal.com/"
    }
    assert data["data"] == expected_data


def test_get_single_competition_fail_not_found_v1(client):
    response = client.get('/v1/competitions/100')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The requested competition was not found"
    }
    assert data["data"] == expected_data


def test_get_single_competition_fail_no_parameter_v1(client):
    response = client.get('/v1/competitions/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert isinstance(data["data"], dict)

    expected_data = {
        "id": 1,
        "last_update": None,
        "name": "A1 Padel Global",
        "url": "https://www.a1padelglobal.com/"
    }
    assert data["data"] == expected_data
    response = client.get('/v1/competitions/1/search?name=&side=')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The search was unsuccessful"
    }
    assert data["data"] == expected_data
