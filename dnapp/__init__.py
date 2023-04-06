import os

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

from dnapp.entities import db, Note, Location, Tag, Campaign, User


app = Flask(__name__)

db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)

login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    from dnapp.auth import auth

    app.register_blueprint(auth)

    from dnapp.api import api

    app.register_blueprint(api)

CORS(app)
