from pony.orm import *
from flask_login import UserMixin

db = Database()


class Note(db.Entity):
    id = PrimaryKey(int, auto=True)
    author = Required("User")
    campaign = Required("Campaign")
    tags = Set("Tag")
    location = Optional("Location")
    date = Required(str)
    time = Required(str)
    text = Required(str)


class Location(db.Entity):
    id = PrimaryKey(int, auto=True)
    notes = Set(Note)
    coord_x = Required(float)
    coord_y = Required(float)
    tags = Set("Tag")
    campaign = Required("Campaign")


class Tag(db.Entity):
    id = PrimaryKey(int, auto=True)
    notes = Set(Note)
    locations = Set(Location)
    text = Required(str)


class Campaign(db.Entity):
    id = PrimaryKey(int, auto=True)
    dm = Required("User", reverse="masters_campaigns")
    players = Set("User", reverse="plays_campaigns")
    nicknames = Set("Nickname", reverse="campaign")
    notes = Set(Note)
    locations = Set(Location)


class Nickname(db.Entity):
    id = PrimaryKey(int, auto=True)
    campaign = Required(Campaign)
    user = Required("User")
    text = Required(str)


class User(db.Entity, UserMixin):
    id = PrimaryKey(int, auto=True)
    email = Required(str)
    password = Required(str)

    masters_campaigns = Set(Campaign, reverse="dm")
    plays_campaigns = Set(Campaign, reverse="players")
    authored_notes = Set(Note)
    nicknames = Set(Nickname, reverse="user")
    opt_ui_dark = Optional(int, size=8, default=0)
    opt_default_nick = Optional(str)
