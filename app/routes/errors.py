# -*- coding: utf-8 -*-
from app import app


@app.errorhandler(404)
def page_not_found(error):
    return {"status": "fail", "data": {"message": "The requested URL does not exist"}}, 404
