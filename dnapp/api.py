from flask import request, redirect, make_response, g, url_for, flash
from flask import Blueprint, render_template, render_template_string
from flask import send_from_directory
from flask import current_app as app
from flask_login import login_required, current_user
from pony.orm import db_session, commit, flush
from dnapp.entities import Note, Campaign, User, Tag
from dnapp import utils
from dnapp.templates import template_strings as TS

api = Blueprint("api", __name__)


@api.route("/static/<filename>")
def static(filename):
    app.logger.debug(filename)
    if filename == "htmx":
        app.logger.warn("redirect to %s", filename)
        return redirect("https://unpkg.com/htmx.org@1.9.0")
    else:
        return send_from_directory("templates", filename)


# TODO broken
def send_invite_email(sender, recipients_mails, campaign):
    app.logger.debug("email??? %s", recipients_mails)
    for recipient_mail in recipients_mails:
        app.logger.debug("email: %s", recipient_mail)
        body = f"""
            Hello!

            You are invited by {sender.email}
            to join his new campaign, {campaign.title}.

            Here's a teaser:
            {campaign.teaser}
            Use this link to join:
            http://google.com/{campaign.title}
        """
        html = f"""
            <p>Hello!</p>
            <p>
                You are invited by {sender.email}
                to join his new campaign, {campaign.title}.
            </p>
            <p>Here's a teaser:</p>
            <p>{campaign.teaser}</p>
            <p>Click here to join:
                <a href='http://google.com'>
                    Dungeon notes: {campaign.title}
                </a>
            </p>
        """
        app.logger.debug("email???")
