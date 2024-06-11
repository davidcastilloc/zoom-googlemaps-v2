# -*- coding: utf-8 -*-
from os import environ


class Config:
    if environ.get("FLASK_ENV") == "development":
        DEBUG = True
        PORT = 5001
    else:
        DEBUG = False
        PORT = 5000
