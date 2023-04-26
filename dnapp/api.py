from flask import request, redirect, make_response, g, url_for, flash
from flask import Blueprint, render_template, render_template_string
from flask import send_from_directory
from flask import current_app as app
from flask_login import login_required, current_user
from pony.orm import db_session, commit, flush
from dnapp.entities import Note, Campaign, User, Tag
from dnapp import utils
from dnapp.templates import template_strings as TS

api_bp = Blueprint("api", __name__)


@api_bp.route("/static/<filename>")
def static(filename):
    app.logger.debug(filename)
    if filename == "htmx":
        app.logger.warn("redirect to %s", filename)
        return redirect("https://unpkg.com/htmx.org@1.9.0")
    else:
        return send_from_directory("templates", filename)
