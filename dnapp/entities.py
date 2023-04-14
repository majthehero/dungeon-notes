from pony.orm import *
from flask_login import UserMixin

db = Database()


class Note(db.Entity):
    id = PrimaryKey(int, auto=True)
    text = Required(str)
    location = Optional("Location")
    date = Required(str)
    time = Required(str)
    tags = Set("Tag")
    campaign = Required("Campaign")
    author = Required("User")


class Location(db.Entity):
    id = PrimaryKey(int, auto=True)
    notes = Set(Note)
    coord_x = Required(float)
    coord_y = Required(float)
    tags = Set("Tag")
    campaign = Required("Campaign")


class Tag(db.Entity):
    id = PrimaryKey(int, auto=True)
    text = Required(str)
    notes = Set(Note)
    locations = Set(Location)


class Campaign(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    notes = Set(Note)
    dm = Required("User", reverse="masters_campaigns")
    players = Set("User", reverse="plays_campaigns")
    locations = Set(Location)


class User(db.Entity, UserMixin):
    id = PrimaryKey(int, auto=True)
    email = Required(str)
    password = Required(str)
    masters_campaigns = Set(Campaign, reverse="dm")
    plays_campaigns = Set(Campaign, reverse="players")
    authored_notes = Set(Note)
