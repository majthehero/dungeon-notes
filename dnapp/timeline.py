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

from dnapp.entities import *
from dnapp import db, utils
from dnapp.templates import template_strings as TS


timeline_bp = Blueprint("timeline", __name__)


@timeline_bp.route("/timeline/<id>", methods=["GET"])
@login_required
def timeline(id):
    notes = None
    with db_session:
        notes = list(Note.select(lambda note: note.campaign.id == id))
        notes_rendered = [
            render_template_string(
                TS.timeline_note, note=note, tools=utils.get_tools("timeline")
            )
            for note in notes
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