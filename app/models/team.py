import datetime

from app import db

# name, location, load (cpu), memory, status

class Team (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    location = db.Column(db.String(150))
    created: datetime.datetime= db.Column(db.DateTime, default=datetime.datetime.now())