from flask import Flask
from flask import request, render_template_string, make_response
from flask_cors import CORS
from dnapp import entities

app = Flask(__name__)


@app.route("/item", methods=["POST", "GET"])
def handle_item():
    app.logger.debug("Hello item")
    if request.method == "GET":
        app.logger.debug("POST /item : %s", request.url)
        return make_response(render_template_string("<p>GET THIS</p>"), 200)
    elif request.method == "POST":
        app.logger.debug("POST /item : %s", request.)
        return make_response(render_template_string("<p>NICE POST :)</p>"), 200)
    else:
        app.logger.warn("wtf")
    return make_response(
        render_template_string("<p>something went wrong in the right way</p>"), 404
    )


CORS(app)
