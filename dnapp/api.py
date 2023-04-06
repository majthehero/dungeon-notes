from flask import request
from flask import Blueprint, request
from flask_login import login_required

api = Blueprint("api", __name__)


@api.route("/home", methods=["GET"])
@login_required
def handle_home():
    return render_template("view.html")


@api.route("/item", methods=["GET", "POST"])
def handle_item():
    if request.method == "GET":
        return "test"

    elif request.method == "POST":
        app.logger.debug("POST /item")
        return make_response(render_template_string("<p>NICE POST :)</p>"), 200)

    return make_response(
        render_template_string("<p>something went wrong in the right way</p>"), 404
    )
