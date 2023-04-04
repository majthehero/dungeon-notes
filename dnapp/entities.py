from pony.orm import *


db = Database()


class Note(db.Entity):
    id = PrimaryKey(int, auto=True)
    location = Optional("Location")
    time = Required(int)
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
    notes = Set(Note)
    locations = Set(Location)


class Campaign(db.Entity):
    id = PrimaryKey(int, auto=True)
    notes = Set(Note)
    master = Required("User", reverse="masters_campaigns")
    players = Set("User", reverse="plays_campaigns")
    locations = Set(Location)


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    masters_campaigns = Set(Campaign, reverse="master")
    plays_campaigns = Set(Campaign, reverse="players")
    authored_notes = Set(Note)


db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)
