import datetime
from dataclasses import dataclass

from app import db

@dataclass
class Application(db.Model):
    application_id: int = db.Column(db.Integer, primary_key = True)
    name: str = db.Column(db.String(150), unique = True)
    owner_id: int = db.Column(db.Integer, db.ForeignKey('user.id'))
    team_name: str = db.Column(db.String(150))
    team_email: str = db.Column(db.String(150))
    url: str = db.Column(db.String(150))
    swagger: str = db.Column(db.String(150))
    bitbucket: str = db.Column(db.String(200), unique = True)
    extra_info: str = db.Column(db.Text(200))
    production_pods: str = db.Column(db.Integer)
    created: datetime.datetime= db.Column(db.DateTime, default=datetime.datetime.now())