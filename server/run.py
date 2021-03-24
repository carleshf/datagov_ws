#!/usr/bin/env python

import logging
from flask import Flask, request, redirect
from flask import url_for
from flask_restplus import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__, static_url_path = '/datagov_ws_service/static')
app.config.from_pyfile('config/config.py')
app.config.update({
	'DEBUG': True,
	'TESTING': True,
	'SECRET_KEY': 'test'
})

cors = CORS(app, resources={r"*": {"origins": "*"}})
db = SQLAlchemy(app)
api = Api(app, doc = '/datagov_ws_service/api/')



from server.database import *
def create_tables():
	db.create_all()
	db.session.commit()

create_tables()


if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 5000, debug = True, threaded = True)