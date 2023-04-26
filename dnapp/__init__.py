import os

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

from dnapp.entities import db, Note, Location, Tag, Campaign, User


app = Flask(__name__)

app.config["SECRET_KEY"] = "wohoo"
db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)

login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    from dnapp.auth import auth_bp

    app.register_blueprint(auth_bp)

    from dnapp.api import api_bp

    app.register_blueprint(api_bp)

    from dnapp.campaign import campaign_bp

    app.register_blueprint(campaign_bp)

    from dnapp.timeline import timeline_bp

    app.register_blueprint(timeline_bp)

CORS(app)
