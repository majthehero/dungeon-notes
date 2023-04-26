import os

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, login_manager
from flask import current_app as app

from pony.orm import db_session

from dnapp.entities import User
from dnapp import db

auth_bp = Blueprint("auth", __name__)


@app.login_manager.user_loader
def load_user(user_id):
    with db_session:
        user = User[user_id]
    return user


@auth_bp.route("/signup", methods=["GET", "POST"])
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
                flash(f"Wellcome, {user.email}, please log in.")
                app.logger.info("signup successfull: welcome - %s", user.email)
                return redirect(url_for("auth.login"))


@auth_bp.route("/", methods=["GET"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        with db_session:
            user = User.get(email=email)

        if user is None or not check_password_hash(user.password, password):
            app.logger.info("login failed: %s", email)
            flash("email and password do not match.")
            return redirect(url_for("auth.login"))

        app.logger.info("login successfull: %s", email)
        flash("Wellcome back, %s", email)
        login_user(user)
        return redirect(url_for("campaign.campaign"))

    return render_template("auth.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
