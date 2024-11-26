import datetime
from dataclasses import dataclass

from sqlalchemy import event

from app import db

@dataclass
class Server (db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(150), unique= True)
    cpu: int = db.Column(db.Integer)
    memory: int = db.Column(db.Integer)
    location: str = db.Column(db.String(150))
    created: datetime.datetime= db.Column(db.DateTime, default=datetime.datetime.now())

# @event.listens_for(Server.__table__, 'after_create')
def create_servers(*args, **kwargs):
    db.session.add(Server(name='ab0001', cpu=123, memory=123, location='Walthamstow'))
    db.session.add(Server(name='ab0002', cpu=234, memory=234, location='Harrow'))
    db.session.add(Server(name='ab0003', cpu=345, memory=345, location='Walthamstow'))
    db.session.add(Server(name='ab0004', cpu=456, memory=456, location='Walthamstow'))
    db.session.add(Server(name='ab0005', cpu=567, memory=567, location='Harrow'))
    db.session.add(Server(name='ab0006', cpu=678, memory=678, location='Walthamstow'))
    db.session.add(Server(name='ab0007', cpu=789, memory=789, location='Walthamstow'))
    db.session.add(Server(name='ab0008', cpu=890, memory=890, location='Harrow'))
    db.session.add(Server(name='ab0009', cpu=901, memory=901, location='Walthamstow'))
    db.session.add(Server(name='ab0010', cpu=184, memory=184, location='Walthamstow'))
    db.session.commit()