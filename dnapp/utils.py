from flask import (
    current_app as app,
    render_template_string,
    make_response,
    render_template,
)
from flask_login import current_user
from pony.orm import db_session
from dnapp.entities import *
from dnapp.templates import template_strings as TS


def parse_players(players: str):
    emails = players.split(",")
    valid_emails = []
    for email in emails:
        if len(email) < 3:
            continue
        if "@" not in email:
            continue
        valid_emails.append(email.strip())
    app.logger.warn("valid emails: %s", valid_emails)
    return valid_emails


def get_tools(page: ""):
    if page == "timeline":
        return []
    else:
        return []


def get_campaigns_by_user():
    user = current_user
    with db_session:
        dms_campaigns = Campaign.select(
            campaign for campaign in Campaign if campaign.dm == current_user
        )
        plays_campaigns = Campaign.select(
            lambda campaign: current_user in campaign.players
        )
        return list(dms_campaigns), list(plays_campaigns)
