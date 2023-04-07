from flask import request, redirect, make_response
from flask import Blueprint, render_template, render_template_string
from flask_login import login_required
from flask import current_app as app

api = Blueprint("api", __name__)


@api.route("/static/<filename>")
def static(filename):
    app.logger.warn("redirect to %s", filename)
    return redirect("https://unpkg.com/" + filename)


@api.route("/home", methods=["GET"])
@login_required
def home():
    return render_template("timeline.html")


@api.route("/item", methods=["GET", "POST"])
def item():
    if request.method == "GET":
        return "test"

    elif request.method == "POST":
        app.logger.debug("POST /item")
        return make_response(render_template_string("<p>NICE POST :)</p>"), 200)

    return make_response(
        render_template_string("<p>something went wrong in the right way</p>"), 404
    )
