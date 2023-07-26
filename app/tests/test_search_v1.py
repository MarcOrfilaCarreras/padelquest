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


def test_get_single_competition_search_v1(client):
    response = client.get('/v1/competitions/1/search')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert len(data["data"]) > 0


def test_get_single_competition_search_fail_not_found_v1(client):
    response = client.get('/v1/competitions/100/search')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "fail"

    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The search was unsuccessful"
    }
    assert data["data"] == expected_data


def test_get_single_competition_search_name_v1(client):
    response = client.get('/v1/competitions/1/search?name=juan')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert len(data["data"]) > 0


def test_get_single_competition_search_name_fail_v1(client):
    response = client.get('/v1/competitions/1/search?name=test')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The search was unsuccessful"
    }
    assert data["data"] == expected_data


def test_get_single_competition_search_side_v1(client):
    response = client.get('/v1/competitions/1/search?side=drive')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert len(data["data"]) > 0


def test_get_single_competition_search_side_fail_v1(client):
    response = client.get('/v1/competitions/1/search?side=test')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The search was unsuccessful"
    }
    assert data["data"] == expected_data


def test_get_single_competition_search_name_side_v1(client):
    response = client.get('/v1/competitions/1/search?name=juan&side=drive')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert len(data["data"]) > 0


def test_get_single_competition_search_name_side_fail_name_v1(client):
    response = client.get('/v1/competitions/1/search?name=test&side=drive')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The search was unsuccessful"
    }
    assert data["data"] == expected_data


def test_get_single_competition_search_name_side_fail_side_v1(client):
    response = client.get('/v1/competitions/1/search?name=juan&side=test')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The search was unsuccessful"
    }
    assert data["data"] == expected_data


def test_get_single_competition_search_name_side_fail_name_side_v1(client):
    response = client.get('/v1/competitions/1/search?name=test&side=test')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The search was unsuccessful"
    }
    assert data["data"] == expected_data


def test_get_single_competition_search_name_side_fail_name_side_no_parameter_v1(client):
    response = client.get('/v1/competitions/1/search?name=&side=')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert isinstance(data["data"], dict)

    expected_data = {
        "message": "The search was unsuccessful"
    }
    assert data["data"] == expected_data
