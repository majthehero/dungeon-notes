import json
from flask import (
    current_app as app,
    Blueprint,
    render_template_string,
    render_template,
    request,
    make_response,
)
from flask_login import login_required, current_user
from pony.orm import db_session

from dnapp.entities import User, Campaign, Note, Location
from dnapp import db, utils
from dnapp.templates import template_strings as TS


timeline_bp = Blueprint("timeline_bp", __name__)


@timeline_bp.route("/timeline/<id>", methods=["GET"])
@login_required
def timeline(id):
    notes = None
    with db_session:
        notes = list(Note.select(lambda note: note.campaign.id == id))
        notes_rendered = [
            render_template_string(TS.timeline_note, note=note) for note in notes
        ]
        return make_response(
            render_template(
                "timeline.html",
                notes=notes_rendered,
                campaign_id=id,
                tools=utils.get_tools("timeline"),
            ),
            200,
        )
    flash("Error loading timeline.")
    return make_response(
        render_template("timeline.html", notes=[], tools=[]),
        500,
    )


@timeline_bp.route("/item", methods=["POST"])
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
        render_string = render_template_string(
            TS.timeline_note, note=n, tools=utils.get_tools("campaign")
        )
        app.logger.info("render string is: %s", render_string)
        return make_response(render_string, 200)
    return make_response("", 500)


@timeline_bp.route("/location/add/1", methods=["POST"])
@login_required
def add_location():
    click_coords = json.loads(request.form.get("clickCoords"))
    x = click_coords["img_x"]
    y = click_coords["img_y"]
    campaign_id = request.form.get("campaign_id")
    app.logger.debug("campaign id in add_loca_1 : %s", campaign_id)
    scale = click_coords["scale"]
    return render_template_string(
        TS.add_location_form, x=x, y=y, scale=scale, campaign_id=campaign_id
    )


@timeline_bp.route("/location/add/2", methods=["POST"])
@login_required
def add_location_2():
    x = request.form.get("x")
    y = request.form.get("y")
    scale = request.form.get("scale")
    name = request.form.get("name")
    description = request.form.get("description")
    campaign_id = request.form.get("campaign_id")
    app.logger.debug("add loc 2 got campaign id %s", campaign_id)
    with db_session:
        camp = Campaign[campaign_id]
        Location(notes=set(), x=x, y=y, campaign=camp, tags=est())
    return "DONE"
