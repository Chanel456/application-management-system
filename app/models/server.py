import datetime
import logging

from sqlalchemy import event
from sqlalchemy.exc import SQLAlchemyError

from app import db

class Server (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique= True)
    cpu = db.Column(db.Integer)
    memory = db.Column(db.Integer)
    location = db.Column(db.String(150))
    created = db.Column(db.DateTime, default=datetime.datetime.now())

@event.listens_for(Server.__table__, 'after_create')
def create_servers(*args, **kwargs):
    """Inserting 10 rows of data into server table on after database creation"""
    try:
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
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('Unable to add dummy data to Server table on database creation')
        logging.error(err)

def fetch_server_with_entity(entity):
    try:
        result = Server.query.with_entities(entity)
        return result
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('An error occurred whilst querying the server table with entity: %s', entity)
        logging.error(err)