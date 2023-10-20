# -*- coding: utf-8 -*-
from app import app


@app.errorhandler(400)
def invalid_argument(error):
    return {"status": "fail", "data": {"message": " Invalid argument"}}, 400


@app.errorhandler(404)
def page_not_found(error):
    return {"status": "fail", "data": {"message": "The requested URL does not exist"}}, 404
