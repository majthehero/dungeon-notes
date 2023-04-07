import os

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, login_manager
from flask import current_app as app

from pony.orm import db_session

from dnapp.entities import User
from dnapp import db


auth = Blueprint("auth", __name__)


@app.login_manager.user_loader
def load_user(user_id):
    with db_session:
        user = User.get(lambda u: u.id == user_id)
    # if user:
    #     app.logger.info("Success - %s - %s", user.id, user.email)
    # else:
    #     app.logger.info("Failed - %s", user_id)
    return user


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("auth.html")

    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        password_1 = request.form.get("password_1")

        if password != password_1:
            app.logger.info("signup failed: password doesn't match itself")
            flash("Typo in password.")
            return redirect(url_for("auth.signup"))

        with db_session:
            taken = User.exists(email=email)
        if taken:
            app.logger.info("signup failed: email taken")
            flash("email already taken.")
            return redirect(url_for("auth.signup"))

        else:
            with db_session:
                user = User(
                    email=email,
                    password=generate_password_hash(password),
                )
            flash("Wellcome, %s", user.email)
            app.logger.info("signup successfull: welcome - %s", user.email)
            return redirect(url_for("api.home"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth.html")

    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        with db_session:
            user = User.get(email=email)
        if (
            user is None
            or not check_password_hash(user.password, password)
            or not login_user(user)
        ):
            app.logger.info("login failed: %", email)
            flash("email and password do not match.")
            return redirect(url_for(auth.login))

        app.logger.info("login successfull: %", email)
        flash("Wellcome back, %s", email)
        return redirect(url_for("api.home"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


# DEBUG
@auth.route("/debug/users")
def get_users():
    with db_session:
        users = User.select()
    app.logger.info("Listing %s users:", users.count())
    for u in users:
        app.logger.info("%s", u.email)
    return "hello"
