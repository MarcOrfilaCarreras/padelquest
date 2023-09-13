# -*- coding: utf-8 -*-
def v1():
    response = {
        "data": {
            "competitions": [
                {
                    "url": "/v1/competitions",
                    "description": "This endpoint returns a list of all competitions."
                },
                {
                    "url": "/v1/competition{competition_id}",
                    "description": "Retrieves the details of a specific competition by its ID. By default, it returns competition 1."
                },
                {
                    "url": "/v1/competition{competition_id}/ranking",
                    "description": "Returns a list of players in a competition, sorted by their ranking. By default, it returns the first 10 players."
                },
                {
                    "url": "/v1/competition{competition_id}/search",
                    "description": "Searches for players in a competition by name and side position. By default, it returns the players with the name of Juan."
                }
            ],
            "players": [
                {
                    "url": "/v1/competition{competition_id}/player/{player_id}",
                    "description": "Retrieves the details of a specific player in a competition by their ID. By default, it returns player 1 of competition 1."
                },
                {
                    "url": "/v1/competition{competition_id}/player/{player_id}/image",
                    "description": "This API route returns the image of a specific player in a given competition."
                }
            ],
            "tournaments": [
                {
                    "url": "/v1/competition{competition_id}/tournaments",
                    "description": "Returns the tournaments of a competition. By default, it returns the current year."
                },
                {
                    "url": "/v1/competition{competition_id}/tournaments/{tournament_id}",
                    "description": "Returns the results of a tournament."
                },
                {
                    "url": "/v1/competition{competition_id}/tournaments/{tournament_id}/image",
                    "description": "Returns the poster of a tournament."
                }
            ]
        },
        "status": "success"
    }

    return response
