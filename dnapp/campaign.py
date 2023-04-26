from flask import (
    current_app as app,
    Blueprint,
    request,
    render_template_string,
    render_template,
    make_response,
)
from flask_login import login_required, current_user
from pony.orm import db_session

from dnapp.entities import *
from dnapp import db, utils
from dnapp.templates import template_strings as TS

campaign_bp = Blueprint("campaign", __name__)


@login_required
@campaign_bp.route(
    "/campaign/",
    defaults={"campaign_id": -1},
    methods=["GET", "POST", "DELETE"],
)
@campaign_bp.route(
    "/campaign/<campaign_id>",
    methods=["GET", "POST", "DELETE"],
)
def campaign(campaign_id):
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


@login_required
@campaign_bp.route(
    "/campaign/<campaign_id>/note/",
    defaults={"note_id": None},
    methods=["GET", "POST", "DELETE"],
)
@campaign_bp.route(
    "/campaign/<campaign_id>/note/<note_id>",
    methods=["GET", "POST", "DELETE"],
)
def note(campaign_id, note_id):
    app.logger.debug("note id", note_id)
    if request.method == "GET":
        return handle_get_note(campaign_id, note_id)
    elif request.method == "POST":
        return handle_post_note(campaign_id, note_id)
    elif request.method == "DELETE":
        return handle_delete_note(campaign_id, note_id)


# region /campaign/<c_id>/note/<n_id> implementation
def handle_get_note(c_id, n_id):
    if n_id is None:
        with db_session:
            notes = Campaign[c_id].notes
            return render_template(
                "timeline.html",
                notes=[
                    render_template_string(TS.timeline_note, note=note)
                    for note in notes
                ],
                campaign_id=c_id,
            )
    else:
        with db_session:
            note = Note[n_id]
            return render_template_string(TS.timeline_note, note=note)


def handle_post_note(c_id, n_id):
    if n_id is None:
        tags = request.form.get("note-tags").split(",")
        tags = map(lambda tag: tag.strip(), tags)
        tags = filter(lambda tag: len(tag) > 0, tags)

        with db_session:
            c = Campaign[c_id]
            u = User[current_user.id]
            n = c.notes.create(
                text=request.form.get("note-text"),
                date="Prvi-Test-DebugEra",
                time="Tik Pred Peto",
                author=u,
            )

            for tag in tags:
                if Tag.exists(lambda t: t.text == tag):
                    Tag.select(lambda t: t.text == tag).first().notes.add(n)
                else:
                    app.logger.debug("TAG: '%s'", tag)
                    Tag(notes=set([n]), text=tag)

            # return render of new tag
            render_string = render_template_string(TS.timeline_note, note=n)
            app.logger.info("render string is: %s", render_string)
            return make_response(render_string, 200)
        return make_response("", 500)


def handle_delete_note(c_id, n_id):
    pass


# region /campaign implementation
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
        # TODO link to a gmail account and set up mailing
        # send_invite_email(current_user, emails_to_send, campaign)
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
