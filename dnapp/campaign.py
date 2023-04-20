from flask import (
    current_app as app,
    Blueprint,
    request,
    render_template_string,
    render_template,
)
from flask_login import login_required, current_user
from pony.orm import db_session

from dnapp.entities import User
from dnapp import db, utils
from dnapp.templates import template_strings as TS

campaign_bp = Blueprint("campaign_bp", __name__)


@login_required
@campaign_bp.route("/campaign", methods=["GET", "POST", "DELETE"])
def campaign():
    if current_user.is_authenticated:
        if request.method == "GET":  # load page
            return handle_campaign_get()
        elif request.method == "POST":  # add element to list of campaigns
            return handle_campaign_post(
                player_emails=request.form.get("players"),
                title=request.form.get("title"),
                teaser=request.form.get("teaser"),
            )
        elif request.method == "DELETE":  # remove element by targeting id
            return handle_campaign_delete(
                command=request.args.get("cmd"),
                campaign_id=request.args.get("id").split("-")[-1],
            )
    app.logger.debug("unknown user")
    return redirect(url_for("auth.login"))


def handle_campaign_get():
    dms_campaigns, plays_campaigns = utils.get_campaigns_by_user()
    campaigns_rendered = [
        render_template_string(TS.dms_campaign_item, campaign=campaign)
        for campaign in dms_campaigns
    ] + [
        render_template_string(TS.plays_campaign_item, campaign=campaign)
        for campaign in plays_campaigns
    ]
    return render_template(
        "campaigns.html",
        campaigns=campaigns_rendered,
        tools=utils.get_tools("campaign"),
    )


def handle_campaign_post(title, player_emails, teaser):
    player_emails = utils.parse_players(player_emails)
    with db_session:
        players = User.select(lambda user: user.email in player_emails)
        # store
        campaign = Campaign(
            title=title,
            dm=User.select(lambda user: user.id == current_user.id).first(),
            players=players,
            teaser=teaser,
        )
        # if email unknown, send email invitation
        emails_to_send = []
        for player in player_emails:
            if not User.exists(lambda user: user.email == player):
                emails_to_send.append(player)

        send_invite_email(current_user, emails_to_send, campaign)
    return make_response(
        render_template_string(TS.dms_campaign_item, campaign=campaign)
    )


def handle_campaign_delete(command, campaign_id):
    if command == "dm-delete":
        with db_session:
            Campaign[campaign_id].delete()
            return render_template_string(TS.campaign_deleted)
    elif command == "player-leave":
        with db_session:
            Campaign[campaign_id].players[current_user.id].remove()
            return render_template_string(TS.campaign_left)
