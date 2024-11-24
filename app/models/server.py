import datetime
from dataclasses import dataclass

from app import db

@dataclass
class Server (db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(150), unique= True)
    cpu: int = db.Column(db.Integer)
    memory: int = db.Column(db.Integer)
    location: str = db.Column(db.String(150))
    created: datetime.datetime= db.Column(db.DateTime, default=datetime.datetime.now())