from flask import request, redirect, make_response, g, url_for, flash
from flask import Blueprint, render_template, render_template_string
from flask_login import login_required, current_user
from flask import current_app as app
from pony.orm import db_session, commit, flush
from dnapp.entities import Note, Campaign, User, Tag
from dnapp import utils
from dnapp.templates import template_strings as TS

api = Blueprint("api", __name__)


@api.route("/static/<filename>")
def static(filename):
    app.logger.warn("redirect to %s", filename)
    return redirect("https://unpkg.com/" + filename)


@api.route("/", methods=["GET"])
@api.route("/campaign", methods=["GET", "POST"])
def campaign():
    app.logger.debug("campaigns")

    if current_user.is_authenticated:
        app.logger.debug(f"known user {current_user.email}")

        if request.method == "GET":  # load page
            dms_campaigns, plays_campaigns = get_campaigns_by_user(current_user)
            return render_template(
                "campaigns.html",
                dms_campaigns=dms_campaigns,
                plays_campaigns=plays_campaigns,
            )

        elif request.method == "POST":  # add element to list of campaigns
            players = request.form.get("players")
            players = utils.parse_players(players)
            with db_session:
                players = User.select(lambda user: user.email in players)
                campaign = Campaign(
                    title=request.form.get("title"),
                    dm=User.select(lambda user: user.id == current_user.id).first(),
                    players=players,
                )
            res = make_response(
                render_template_string(TS.campaign_list_item, campaign=campaign)
            )
            app.logger.warn(res)
            return res
        elif request.method == "DELETE":  # remove element by targeting id
            with db_session:
                Campaign[int(request.form.id.split("-")[-1])].delete()
                return render_template_string(TS.campaign_list_item_deleted)

    app.logger.debug("unknown user")
    return redirect(url_for("auth.login"))


def get_campaigns_by_user(user):
    with db_session:
        dms_campaigns = Campaign.select(lambda campaign: campaign.dm == current_user)
        plays_campaigns = Campaign.select(
            lambda campaign: current_user in campaign.players
        )
        return list(dms_campaigns), list(plays_campaigns)


@api.route("/timeline/<id>")
@login_required
def timeline(id):
    notes = None
    with db_session:
        notes = list(Note.select(lambda note: note.campaign.id == id))
        return make_response(
            render_template("timeline.html", notes=notes, campaign_id=id),
            200,
        )
    flash("Error loading timeline.")
    return make_response(render_template("timeline.html", notes=[]), 500)


@api.route("/item", methods=["POST"])
@login_required
def item():
    app.logger.info("got item post request")

    campaign_id = request.form.get("note-campaign-id")

    tags = request.form.get("note-tags").split(",")
    tags = map(lambda tag: tag.strip(), tags)
    tags = filter(lambda tag: len(tag) > 0, tags)

    app.logger.debug("tags: %s", list(tags))

    with db_session:
        # make note
        c = Campaign[campaign_id]
        u = User[current_user.id]
        n = c.notes.create(
            text=request.form.get("note-text"),
            date="Prvi-Test-DebugEra",
            time="Tik Pred Peto",
            author=u,
        )
        app.logger.debug("n: %s", n)

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
